from __future__ import absolute_import

import flask
from flask.views import MethodView
from webargs import fields
from webargs.flaskparser import use_args

from rmfdb.web.stigs.models import Rule, Stig
from rmfdb.web.stigs.schema import (
    rule_schema,
    rules_schema,
    stig_schema,
    stigs_schema,
)


__all__ = (
    'stigs',
)

stigs = flask.Blueprint('stigs', __name__)


class StigsView(MethodView):

    @use_args({
        'page': fields.Int(missing=0),
        'pageSize': fields.Int(missing=5)
    })
    def get(self, reqargs):
        page = reqargs.get('page', 0) + 1
        page_size = reqargs.get('pageSize', 5)
        stigs = Stig.query.order_by(Stig.release_date.desc()).paginate(
            page=page, per_page=page_size)
        return flask.jsonify(
            total=stigs.total,
            stigs=stigs_schema.dump(stigs.items)[0]
        )


class StigVersionsView(MethodView):

    def get(self, id):
        stig = Stig.query.filter_by(id=id).first_or_404()
        stig_versions = Stig.query.filter_by(name=stig.name).order_by(
            Stig.release_date.desc()).all()
        return stigs_schema.jsonify(stig_versions.remove(stig))


class StigView(MethodView):

    def get(self, id):
        stig = Stig.query.filter_by(id=id).first_or_404()
        return stig_schema.jsonify(stig)


class RuleView(MethodView):

    def get(self, id):
        rule = Rule.query.filter_by(full_rule_id=id).first_or_404()
        return rule_schema.jsonify(rule)


class RuleVersionsView(MethodView):

    def get(self, rule_id):
        rule_versions = Rule.query.filter_by(rule_id=rule_id).all()
        return rules_schema.jsonify(rule_versions)


stigs.add_url_rule(
    '/stigs',
    view_func=StigsView.as_view('stigs_view'),
    methods=('GET',))
stigs.add_url_rule(
    '/stigs/<string:id>',
    view_func=StigView.as_view('stig_view'),
    methods=('GET',))
stigs.add_url_rule(
    '/stigs/<string:id>/versions',
    view_func=StigVersionsView.as_view('stig_versions_view'),
    methods=('GET',))
stigs.add_url_rule(
    '/rules/<string:id>',
    view_func=RuleView.as_view('rule_view'),
    methods=('GET',))
stigs.add_url_rule(
    '/rules/<string:rule_id>/versions',
    view_func=RuleVersionsView.as_view('rule_versions_view'),
    methods=('GET',))
