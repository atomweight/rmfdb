from __future__ import absolute_import

from marshmallow import fields
from marshmallow_enum import EnumField

from rmfdb.web.controls.models import Cci, Control, LowModHigh
from rmfdb.web.middleware import ma


__all__ = (
    'cci_schema',
    'ccis_schema',
    'control_schema',
    'controls_schema',
)


class CciSchema(ma.ModelSchema):

    control = fields.Nested(
        'ControlSchema',
        exclude=['ccis'],
    )

    class Meta(object):  # noqa: D101

        model = Cci
        exclude = ['search_vector']


class ControlSchema(ma.ModelSchema):

    confidentiality_threshold = EnumField(LowModHigh)
    integrity_threshold = EnumField(LowModHigh)
    availability_threshold = EnumField(LowModHigh)
    ccis = fields.Nested(
        CciSchema,
        many=True,
        exclude=['control'])

    class Meta(object):  # noqa: D101

        model = Control
        exclude = ['search_vector']


cci_schema = CciSchema()
ccis_schema = CciSchema(many=True)
control_schema = ControlSchema()
controls_schema = ControlSchema(many=True)
