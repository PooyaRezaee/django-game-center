from .base import *

ALLOWED_HOSTS = [
    "*"
]
INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

TIME_CACHE_VIEW = 60
SOLO_CACHE = 'default'
SOLO_CACHE_TIMEOUT = TIME_CACHE_VIEW