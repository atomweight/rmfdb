from __future__ import absolute_import

import hashlib
import json

import click
import flask
from lxml import html
import pkg_resources
import requests
import sqlalchemy

from rmfdb.parser import process_stig_zips
import rmfdb.web.app
from rmfdb.web.controls.models import Cci, Control, LowModHigh
from rmfdb.web.middleware import db
from rmfdb.web.stigs.models import StigLibrary


FIXTURE_DIR = pkg_resources.resource_filename('rmfdb', 'fixtures')


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = rmfdb.web.app.create_app()


@main.command()
@click.option('--local-file', default=None)
@click.option('--force', flag_value=True)
@click.pass_obj
def download_stigs(app, local_file, force):
    with app.app_context():
        if local_file:
            library_file = open(local_file, 'rb')
            library_file_content = library_file.read()
            library_file.close()
        else:
            flask.current_app.logger.info(
                'Checking DISA for new masterlist release')
            stig_page = requests.get(
                'https://iase.disa.mil/stigs/Lists/stigs-masterlist/'
                'stig-srg-compilation-qtr.aspx')
            stig_page_html = html.fromstring(stig_page.content)
            links = stig_page_html.xpath('//a/@href')
            download_library_link = None
            for link in links:
                if 'U_SRG-STIG_Library' in link:
                    flask.current_app.logger.info(
                        'Found link to STIG compilation library')
                    download_library_link = link
            if not download_library_link:
                # todo - handle failure
                flask.current_app.logger.info(
                    'Did not find link to STIG compilation library, '
                    'exiting...')
                return
            flask.current_app.logger.info(
                'Downloading STIG compilation library from "{}"...'.format(
                    download_library_link))
            library_file_content = requests.get(download_library_link).content
        library_file_hash = hashlib.sha512()
        library_file_hash.update(library_file_content)
        library_file_hash_string = library_file_hash.hexdigest()
        flask.current_app.logger.debug(
            'Hash of STIG compilation library is "{}"'.format(
                library_file_hash_string))
        library_result = StigLibrary.query.filter_by(
            hash_value=library_file_hash_string).first()
        if not library_result:
            flask.current_app.logger.info(
                'This is a new STIG compilation library, '
                'adding to database...')
            library = StigLibrary(hash_value=library_file_hash_string)
            db.session.add(library)
            db.session.commit()
        else:
            if not force:
                flask.current_app.logger.info(
                    'This is not a new STIG compilation library, exiting...')
                return
        process_stig_zips(library_file_content)


@main.command()
@click.pass_obj
def seed_control_data(app):
    with app.app_context():
        controls_json = open('{}/800-53r4.json'.format(FIXTURE_DIR))
        controls = json.load(controls_json)
        for control in controls:
            try:
                control_obj = Control(
                    control_id=control.get('id'),
                    family=control.get('family'),
                    family_acronym=control.get('family_abbrev'),
                    text=control.get('definition'),
                    guidance=control.get('guidance'),
                    name=control.get('name'),
                    confidentiality_threshold=LowModHigh(
                        control.get('confidentiality_threshold')),
                    integrity_threshold=LowModHigh(
                        control.get('integrity_threshold')),
                    availability_threshold=LowModHigh(
                        control.get('availability_threshold')),
                )
                db.session.add(control_obj)
                db.session.commit()
                for cci in control.get('ccis'):
                    cci_obj = Cci(
                        control=control_obj,
                        cci_id=cci.get('id'),
                        ap_acronym=cci.get('ap_acronym'),
                        text=cci.get('definition'),
                        auditor_guidance=cci.get('guidance_auditor'),
                        org_guidance=cci.get('guidance_org'),
                    )
                    db.session.add(cci_obj)
                    db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                # flask.current_app.logger.error(
                #     'Controls have already been seeded!')
                db.session.rollback()
                continue
        controls_json.close()
