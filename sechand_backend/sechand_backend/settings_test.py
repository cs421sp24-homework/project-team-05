from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oose_test',
        'USER': 'sechandtest',
        'PASSWORD': '12qwaszx',
        'HOST': 'database-1.cx2g2ywcaj8r.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}