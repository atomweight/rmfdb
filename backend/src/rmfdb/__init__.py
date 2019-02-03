from __future__ import absolute_import

import pkg_resources


try:  # pragma: no cover
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'
