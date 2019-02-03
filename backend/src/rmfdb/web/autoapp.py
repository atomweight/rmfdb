from __future__ import absolute_import

import os

from rmfdb.web.app import create_app


__all__ = ('app',)


app = create_app(config_path=os.getenv('RMFDB_CONFIG', 'config.json'))
