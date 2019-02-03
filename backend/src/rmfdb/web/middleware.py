from __future__ import absolute_import

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import flask_marshmallow
import flask_migrate
import flask_sqlalchemy
import flask_talisman


db = flask_sqlalchemy.SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
ma = flask_marshmallow.Marshmallow()
migrate = flask_migrate.Migrate()
talisman = flask_talisman.Talisman()
