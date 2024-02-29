from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'oosesechand',
        'PASSWORD': 'aswids$@213yu87diu1734#^*&hSDJDUEHA&Saosd',
        'HOST': 'sechand-test.postgres.database.azure.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require'
        },
    }
}