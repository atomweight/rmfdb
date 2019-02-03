from __future__ import absolute_import

import datetime
import enum
import uuid

from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType

from rmfdb.web.middleware import db


class StigLibrary(db.Model):
    __tablename__ = 'stig_library'

    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    hash_value = db.Column('hash', db.Unicode(128), nullable=False, unique=True)
    date_downloaded = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )

class StigQuery(BaseQuery, SearchQueryMixin):
    pass


class Stig(db.Model):
    __tablename__ = 'stigs'
    __table_args__ = (db.UniqueConstraint(
        'name', 'version', 'release', name='_stig_uc'),)
    query_class = StigQuery

    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.UnicodeText)
    version = db.Column(db.Integer, nullable=False)
    release = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
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
            'name',
            'description',
        )
    )


class RuleSeverity(enum.Enum):

    INFORMATIONAL = INFO = 'info'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


cve_rule_mapping_table = db.Table(
    'cve_rule_mappings',
    db.Model.metadata,
    db.Column(
        'rule_id', UUIDType(binary=False),
        db.ForeignKey('rules.id'),
        nullable=False),
    db.Column(
        'cve_id', db.Unicode,
        db.ForeignKey('cves.id'),
        nullable=False),
    db.UniqueConstraint(
        'rule_id', 'cve_id',
        name='_rule_cve_uc')
)


class CVE(db.Model):
    __tablename__ = 'cves'

    id = db.Column(db.Unicode, primary_key=True, nullable=False, unique=True)


stig_rule_mapping_table = db.Table(
    'stig_rule_mappings',
    db.Model.metadata,
    db.Column(
        'rule_id', UUIDType(binary=False),
        db.ForeignKey('rules.id'),
        nullable=False),
    db.Column(
        'stig_id', UUIDType(binary=False),
        db.ForeignKey('stigs.id'),
        nullable=False),
    db.UniqueConstraint(
        'rule_id', 'stig_id',
        name='_rule_stig_uc')
)

cci_rule_mapping_table = db.Table(
    'cci_rule_mappings',
    db.Model.metadata,
    db.Column(
        'rule_id', UUIDType(binary=False),
        db.ForeignKey('rules.id'),
        nullable=False),
    db.Column(
        'cci_id', UUIDType(binary=False),
        db.ForeignKey('ccis.id'),
        nullable=False),
    db.UniqueConstraint(
        'rule_id', 'cci_id',
        name='_rule_cci_uc')
)


class RuleQuery(BaseQuery, SearchQueryMixin):
    pass


class Rule(db.Model):
    __tablename__ = 'rules'
    query_class = RuleQuery

    id = db.Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    group_id = db.Column(db.Unicode, nullable=False)
    group_title = db.Column(db.Unicode, nullable=False)
    full_rule_id = db.Column(db.Unicode, nullable=False, unique=True)
    rule_id = db.Column(db.Unicode, nullable=False)
    rule_revision = db.Column(db.Integer, nullable=False)
    rule_severity = db.Column(db.Enum(RuleSeverity), nullable=False)
    rule_title = db.Column(db.Unicode, nullable=False)
    rule_metadata = db.Column('metadata', db.JSON)
    check_content = db.Column(db.UnicodeText, nullable=False)
    fix_text = db.Column(db.UnicodeText, nullable=False)
    cves = db.relationship(
        'CVE',
        secondary=cve_rule_mapping_table,
        backref=db.backref(
            'rules',
            lazy=False),
        lazy=False)
    ccis = db.relationship(
        'Cci',
        secondary=cci_rule_mapping_table,
        backref=db.backref('rules', lazy=False),
        lazy=False
    )
    stigs = db.relationship(
        'Stig',
        secondary=stig_rule_mapping_table,
        backref=db.backref('rules', lazy=False),
        lazy=False
    )
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
            'group_id',
            'group_title',
            'full_rule_id',
            'rule_title',
            'check_content',
            'fix_text',
        )
    )
