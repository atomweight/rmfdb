from __future__ import absolute_import

import flask.views

import rmfdb
from rmfdb.web.stigs.models import StigLibrary


__all__ = ('settings',)

settings = flask.Blueprint('settings', __name__)


class VersionView(flask.views.MethodView):

    def get(self):
        """Returns the version of the app and last updated time."""
        version = rmfdb.__version__
        last_updated = StigLibrary.query.order_by(
            StigLibrary.date_downloaded.desc()).first()
        return flask.jsonify(
            version=version,
            lastUpdated=(
                last_updated.date_downloaded if last_updated else 'None'
            )
        )


settings.add_url_rule(
    '/version',
    view_func=VersionView.as_view('version_view'),
    methods=('GET',))
