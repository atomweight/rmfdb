from __future__ import absolute_import

import binascii
import json
import logging
import os

import flask
from sqlalchemy_searchable import make_searchable

from rmfdb.web.controls.views import controls
import rmfdb.web.middleware as middleware
from rmfdb.web.search.views import search
from rmfdb.web.settings.views import settings
from rmfdb.web.stigs.views import stigs


__all__ = (
    'create_app',
)

default_config_filename = 'config.json'
default_config = {
    'DEBUG': False,
    'SECRET_KEY': binascii.hexlify(os.urandom(24)).decode('utf-8'),
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'CACHE_TYPE': 'simple',
}


def create_app(config_path=None, name=None):
    """Create a Flask application.

    Args:
        config_path (str, optional): The absolute or relative path to
            the JSON formatted configuration file. If not provided,
            defaults to *config.json*.
        name (str, optional): The name of the Flask application.
            Defaults to the name of the package.

    Returns:
        :class:`flask.Flask`: A Flask application instance.

    """
    if name is None:
        name = __name__.split('.')[0]
    app = flask.Flask(name, instance_relative_config=True)
    if config_path is None:
        config_path = os.getenv('RMFDB_CONFIG', default_config_filename)
    init_config(app, config_path=config_path)
    for key in app.config:
        envvar = key.upper()
        if envvar in os.environ:
            app.config[key] = os.getenv(envvar)
    app.logger.setLevel(logging.INFO)
    init_handlers(app)

    # middleware
    middleware.cache.init_app(app)
    middleware.db.init_app(app)
    middleware.limiter.init_app(app)
    middleware.ma.init_app(app)
    middleware.migrate.init_app(app, middleware.db)
    middleware.talisman.init_app(app, force_https=False)
    # fts
    make_searchable(middleware.db.metadata)
    middleware.db.configure_mappers()

    # blueprints
    app.register_blueprint(settings)
    app.register_blueprint(stigs)
    app.register_blueprint(controls)
    app.register_blueprint(search)

    return app


def init_config(app, config_path='config.json'):
    """Read application configuration from a local JSON file."""
    if not os.path.isabs(config_path):
        config_path = os.path.join(app.instance_path, config_path)
    try:
        app.config.from_json(config_path)
    except FileNotFoundError:
        app.logger.warn('Initializing default config at %s', config_path)
        if not os.path.exists(os.path.dirname(config_path)):
            os.makedirs(os.path.dirname(config_path))
        with app.open_instance_resource(config_path, 'w') as f:
            json.dump(default_config, f)
        app.config.from_json(config_path)

    # hardcode application defaults - handle debug case to disable
    # certain security configurations for staging/dev
    debug = app.config.get('DEBUG', False)
    app.config.update(
        {
            'DEBUG': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': True,
        }
    )
    if debug:
        app.config.update(
            {
                'ENV': 'development',
                'TESTING': True,
            }
        )


def init_handlers(app):
    """Initialize application error handlers."""
    app.errorhandler(404)(on_404)
    app.errorhandler(403)(on_403)
    app.errorhandler(400)(on_validation_error)
    app.errorhandler(422)(on_validation_error)  # XXX: ???


def on_validation_error(error):
    payload = {'code': 400, 'message': 'Bad request.'}
    try:
        payload['errors'] = error.exc.messages
    except AttributeError:
        payload['errors'] = ['Bad request.']
    response = flask.jsonify(**payload)
    response.status_code = 400
    return response


def on_403(error):
    response = flask.jsonify(code=403, message='Access forbidden.')
    response.status_code = 403
    return response


def on_404(error):
    response = flask.jsonify(code=404, message='Resource not found.')
    response.status_code = 404
    return response
