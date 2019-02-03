from __future__ import absolute_import

from marshmallow import fields
from marshmallow_enum import EnumField

from rmfdb.web.middleware import ma
from rmfdb.web.stigs.models import CVE, Rule, RuleSeverity, Stig


__all__ = (
    'cve_schema',
    'cves_schema',
    'rule_schema',
    'rules_schema',
    'stig_schema',
    'stigs_schema',
    'CVESchema',
    'RuleSchema',
    'StigSchema',
)


class CVESchema(ma.ModelSchema):

    class Meta(object):  # noqa: D101

        model = CVE


class StigSchema(ma.ModelSchema):

    rules = fields.Nested(
        'RuleSchema',
        many=True,
        exclude=('stigs',),
    )

    class Meta(object):  # noqa: D101

        model = Stig
        exclude = ['search_vector']


class RuleSchema(ma.ModelSchema):

    rule_severity = EnumField(RuleSeverity, by_value=True)
    ccis = fields.Nested(
        'CciSchema',
        many=True,
        exclude=['rules', 'control'],
    )
    stigs = fields.Nested(
        'StigSchema',
        many=True,
        exclude=['rules'],
    )

    class Meta(object):  # noqa: D101

        model = Rule
        exclude = ['search_vector']


cve_schema = CVESchema()
cves_schema = CVESchema(many=True)
stig_schema = StigSchema()
stigs_schema = StigSchema(many=True, exclude=['rules'])
rule_schema = RuleSchema()
rules_schema = RuleSchema(many=True)
cci_rules_schema = RuleSchema(many=True, exclude=['ccis'])
