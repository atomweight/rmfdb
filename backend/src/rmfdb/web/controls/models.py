from __future__ import absolute_import

import datetime
import enum
import uuid

from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType

from rmfdb.web.middleware import db


class LowModHigh(enum.Enum):

    LOW = 0
    MODERATE = 1
    HIGH = 2
    NONE = 3


class ControlQuery(BaseQuery, SearchQueryMixin):
    pass


class Control(db.Model):
    __tablename__ = 'controls'
    query_class = ControlQuery

    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    control_id = db.Column(db.Unicode, unique=True, nullable=False)
    family = db.Column(db.Unicode, nullable=False)
    family_acronym = db.Column(db.Unicode, nullable=False)
    text = db.Column(db.UnicodeText, nullable=False)
    name = db.Column(db.Unicode, nullable=False)
    guidance = db.Column(db.UnicodeText)
    confidentiality_threshold = db.Column(db.Enum(LowModHigh), nullable=False)
    integrity_threshold = db.Column(db.Enum(LowModHigh), nullable=False)
    availability_threshold = db.Column(db.Enum(LowModHigh), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    search_vector = db.Column(
        TSVectorType(
            'control_id',
            'family',
            'family_acronym',
            'text',
            'name',
            'guidance',
        )
    )


class CciQuery(BaseQuery, SearchQueryMixin):
    pass


class Cci(db.Model):
    __tablename__ = 'ccis'
    query_class = CciQuery

    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    cci_id = db.Column(db.Unicode, unique=True, nullable=False)
    ap_acronym = db.Column(db.Unicode)
    text = db.Column(db.UnicodeText)
    auditor_guidance = db.Column(db.UnicodeText)
    org_guidance = db.Column(db.UnicodeText)
    control_id = db.Column(
        UUIDType(binary=False), db.ForeignKey('controls.id'))
    control = db.relationship(
        'Control', backref='ccis')
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    search_vector = db.Column(
        TSVectorType(
            'cci_id',
            'ap_acronym',
            'text',
            'auditor_guidance',
            'org_guidance',
        )
    )
