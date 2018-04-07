# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .base import *


DEBUG = True

SECRET_KEY = 'random'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '95fe8261.ngrok.io'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

