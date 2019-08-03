from __future__ import absolute_import

import flask
from flask.views import MethodView
from webargs import fields
from webargs.flaskparser import use_args

from rmfdb.web.controls.models import Cci, Control
from rmfdb.web.controls.schema import (
    ccis_schema,
    controls_schema,
)
from rmfdb.web.stigs.models import Rule, Stig
from rmfdb.web.stigs.schema import (
    rules_schema,
    stigs_schema,
)

__all__ = (
    'search',
)

search = flask.Blueprint('search', __name__)


class SearchView(MethodView):

    @use_args({
        'query': fields.Str(required=True),
    })
    def post(self, reqargs):
        query = reqargs['query']
        stig_results = Stig.query.search(
            query).order_by(Stig.release_date.desc()).all()
        rule_results = Rule.query.search(
            query).order_by(Rule.created_at.desc()).all()
        cci_results = Cci.query.search(query).all()
        ctrl_results = Control.query.search(query).all()
        return flask.jsonify(
            stigs=stigs_schema.dump(stig_results).data,
            rules=rules_schema.dump(rule_results).data,
            ccis=ccis_schema.dump(cci_results).data,
            controls=controls_schema.dump(ctrl_results).data,
        )


search.add_url_rule(
    '/api/search',
    view_func=SearchView.as_view('search_view'),
    methods=('POST',))
