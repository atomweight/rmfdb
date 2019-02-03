from __future__ import absolute_import

import flask
from flask.views import MethodView
from webargs import fields
from webargs.flaskparser import use_args

from rmfdb.web.controls.models import Cci, Control
from rmfdb.web.controls.schema import (
    cci_schema,
    control_schema,
    controls_schema,
)
from rmfdb.web.middleware import cache
from rmfdb.web.stigs.schema import cci_rules_schema


__all__ = (
    'controls',
)

controls = flask.Blueprint('controls', __name__)


class ControlsView(MethodView):

    @use_args({
        'page': fields.Int(missing=0),
        'pageSize': fields.Int(missing=5)
    })
    def get(self, reqargs):
        page = reqargs.get('page', 0) + 1
        page_size = reqargs.get('pageSize', 5)
        controls = Control.query.order_by(Control.created_at.asc()).paginate(
            page=page, per_page=page_size)
        return flask.jsonify(
            total=controls.total,
            controls=controls_schema.dump(controls.items)[0]
        )


class ControlView(MethodView):

    @cache.cached(timeout=86400)
    def get(self, ctrl_id):
        control = Control.query.filter_by(control_id=ctrl_id).first_or_404()
        return control_schema.jsonify(control)


class CciView(MethodView):

    @cache.cached(timeout=86400)
    def get(self, cci_id):
        cci = Cci.query.filter_by(cci_id=cci_id).first_or_404()
        return cci_schema.jsonify(cci)


class CciRulesView(MethodView):

    @cache.cached(timeout=86400)
    def get(self, cci_id):
        cci = Cci.query.filter_by(cci_id=cci_id).first_or_404()
        return flask.jsonify(
            cci_rules_schema.dump(cci.rules)[0]
        )


controls.add_url_rule(
    '/controls',
    view_func=ControlsView.as_view('controls_view'),
    methods=('GET',))
controls.add_url_rule(
    '/controls/<string:ctrl_id>',
    view_func=ControlView.as_view('control_view'),
    methods=('GET',))
controls.add_url_rule(
    '/ccis/<string:cci_id>',
    view_func=CciView.as_view('cci_view'),
    methods=('GET',))
controls.add_url_rule(
    '/ccis/<string:cci_id>/rules',
    view_func=CciRulesView.as_view('cci_rules_view'),
    methods=('GET',))
