from __future__ import absolute_import

import datetime
from io import BytesIO
import os
import re
import shutil
from zipfile import ZipFile

import defusedxml.cElementTree as ElementTree
import flask

from rmfdb.web.controls.models import Cci
from rmfdb.web.middleware import db
import rmfdb.web.stigs.models as stig_models


XCCDF_1_1 = '{http://checklists.nist.gov/xccdf/1.1}'


class ParseError(Exception):
    pass


def get_elem_text(elem, default=''):
    """Convenience function for retrieving text form an ElementTree node."""
    return (elem.text or default if elem is not None else default).strip()


def process_stig_zips(library_file_content):
    library_file = ZipFile(BytesIO(library_file_content))
    unzip_location = os.path.join(
        flask.current_app.instance_path, 'stigs-tmp')
    for ffile in library_file.namelist():
        if '_STIG.zip' in ffile or '_SRG.zip' in ffile:
            flask.current_app.logger.info('Found STIG ZIP "{}"'.format(ffile))
            stig_zip = library_file.extract(ffile, unzip_location)
            stig_zip_file = ZipFile(stig_zip)
            for possible_stig in stig_zip_file.namelist():
                if '-xccdf.xml' in possible_stig and '~$' not in possible_stig:
                    flask.current_app.logger.info(
                        'Found XCCDF "{}" within STIG zip, parsing...'.format(
                            possible_stig))
                    stig_xccdf = stig_zip_file.extract(
                        possible_stig, unzip_location)
                    parse_stig(stig_xccdf)
    flask.current_app.logger.info('Processed all STIGs, cleaning up...')
    shutil.rmtree(unzip_location)


def parse_stig(stig_location):
    with open(stig_location, 'rb') as stig_file:
        contents = stig_file.read()
    tree = ElementTree.fromstring(contents)

    # parse name
    try:
        stig_name = tree.find('{}title'.format(XCCDF_1_1)).text.strip()
    except AttributeError:
        raise ParseError('title element not present in STIG')

    # parse description, version & release date
    description = get_elem_text(tree.find('{}description'.format(XCCDF_1_1)))
    version = tree.find('{}version'.format(XCCDF_1_1))
    plain_text = tree.find('{}plain-text'.format(XCCDF_1_1))
    if None in (version, plain_text):
        raise ParseError('version info missing from STIG')
    release_info = re.match(
        r'Release:\s+(\d+)\sBenchmark\sDate:\s+(.*)', plain_text.text, re.I)
    if release_info is None:
        raise ParseError('Unable to parse release-info: {}'.format(
            plain_text.text))
    version_text = version.text
    release_num = release_info.group(1)
    release_date = release_info.group(2)

    # try to parse dates correctly because DISA
    try:
        release_datetime = datetime.datetime.strptime(release_date, '%d %b %Y')
    except ValueError:
        release_datetime = datetime.datetime.strptime(release_date, '%d %B %Y')

    stig = stig_models.Stig.query.filter_by(
        name=stig_name,
        version=version_text,
        release=release_num).first()
    if not stig:
        stig = stig_models.Stig(
            name=stig_name,
            description=description,
            version=version_text,
            release=release_num,
            release_date=release_datetime)
        db.session.add(stig)
        db.session.commit()

    # parse checks
    groups = tree.findall('{}Group'.format(XCCDF_1_1))
    profiles = tree.findall('{}Profile'.format(XCCDF_1_1))
    for group in groups:
        group_id = group.get('id')

        group_title = get_elem_text(group.find(
            '{}title'.format(XCCDF_1_1)))

        stig_profiles = []
        for profile in profiles:
            selector = '{}select[@idref=\'{}\'][@selected=\'true\']'.format(
                XCCDF_1_1, group_id)
            if profile.find(selector) is not None:
                stig_profiles.append(profile.get('id'))
        for rule in group.findall('{}Rule'.format(XCCDF_1_1)):
            unparsed_rule_id = rule.get('id')
            full_rule_id = re.match(
                r'(.*)r(\d+)_rule', unparsed_rule_id, re.I)
            rule_id = full_rule_id.group(1)
            rule_revision = full_rule_id.group(2)

            rule_severity = rule.get('severity')

            rule_title = get_elem_text(rule.find(
                '{}title'.format(XCCDF_1_1)))

            # yo dawg we heard you like XML so we put (sometimes) HTML
            # escaped XML in your XML so you can parse XML while you parse
            # XML! - #DISA2012
            metadata = dict(re.findall(
                r'(?:&lt;|<)(?P<tag>.+?)(?:&gt;|>)'
                '(?P<value>.+?)(?:&lt;|<)/(?P=tag)(?:&gt;|>)',
                get_elem_text(rule.find(
                    '{}description'.format(XCCDF_1_1))),
                re.IGNORECASE + re.DOTALL + re.MULTILINE + re.UNICODE
            ))
            metadata.update({
                'mac_profiles': stig_profiles,
                'version': get_elem_text(rule.find('{}version'.format(
                    XCCDF_1_1))),
            })

            check_content = rule.find('.//{}check-content'.format(
                XCCDF_1_1))
            if check_content is not None:
                check_content = check_content.text
            else:
                check_content = rule.find('.//{}check-content-ref'.format(
                    XCCDF_1_1))
                if check_content is not None:
                    check_content = check_content.get('name')
                else:
                    check_content = 'No check content given'

            fix_text = rule.find('{}fixtext'.format(XCCDF_1_1))
            if fix_text is not None:
                fix_text = fix_text.text
            else:
                fix_text = 'No fix text given'

            cves = [get_elem_text(ident)
                    for ident in rule.findall(
                    '{}ident'
                    '[@system=\'http://cve.mitre.org\']'.format(
                        XCCDF_1_1)) or []]
            cve_objects = []
            for cve in cves:
                cve_object = stig_models.CVE.query.filter_by(id=cve).first()
                if not cve_object:
                    cve_object = stig_models.CVE(id=cve)
                    db.session.add(cve_object)
                    db.session.commit()
                cve_objects.append(cve_object)

            ccis = [get_elem_text(ident)
                    for ident in rule.findall(
                    '{}ident'
                    '[@system=\'http://iase.disa.mil/cci\']'.format(
                        XCCDF_1_1)) or []]
            cci_objects = []
            for cci in ccis:
                cci_object = Cci.query.filter_by(cci_id=cci).first()
                if not cci_object:
                    flask.current_app.logger.warn(
                        'Found non-existent CCI {}, creating it...'.format(
                            cci))
                    cci_object = Cci(cci_id=cci)
                    db.session.add(cci_object)
                    db.session.commit()
                cci_objects.append(cci_object)

            # try to insert rule
            rule = stig_models.Rule.query.filter_by(
                full_rule_id=unparsed_rule_id).first()
            if rule:
                flask.current_app.logger.info(
                    'Found existing rule "{}"'.format(unparsed_rule_id))
                if rule not in stig.rules:
                    flask.current_app.logger.info(
                        'Rule "{}" was not in STIG "{}", adding it...'.format(
                            unparsed_rule_id, stig_name))
                    stig.rules.append(rule)
                    db.session.commit()
            else:
                flask.current_app.logger.info(
                    'Creating new rule "{}" in STIG "{}"'.format(
                        unparsed_rule_id, stig_name))
                rule = stig_models.Rule(
                    group_id=group_id,
                    group_title=group_title,
                    full_rule_id=unparsed_rule_id,
                    rule_id=rule_id,
                    rule_revision=rule_revision,
                    rule_severity=stig_models.RuleSeverity(rule_severity),
                    rule_title=rule_title,
                    rule_metadata=metadata,
                    check_content=check_content,
                    fix_text=fix_text,
                    cves=cve_objects,
                    ccis=cci_objects,
                )
                db.session.add(rule)
                stig.rules.append(rule)
                db.session.commit()
