# -*- coding: utf-8 -*-
from django.conf import settings as django_settings


SETTINGS = (
    {
        'name': 'BK_AZURE_ACCOUNT_NAME',
        'default': None
    },
    {
        'name': 'BK_AZURE_ACCOUNT_KEY',
        'default': None
    },
    {
        'name': 'BK_AZURE_CONTAINER',
        'default': None
    },
    {
        'name': 'BK_LOCAL_PATHS',
        'default': []
    }
)

for setting in SETTINGS:
    value = getattr(django_settings, setting['name'], setting['default'])
    globals()[setting['name']] = value