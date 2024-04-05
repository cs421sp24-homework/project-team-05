from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sechandtestdb',
        'USER': 'testuser',
        'PASSWORD': 'testuser123456',
        'HOST': 'testdb.cx2g2ywcaj8r.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}