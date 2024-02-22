# Include the following the script to use the psql server:
# export DJANGO_USE_PSQL=true
# This will override the DATABASES variable in settings.py

# Use Postgresql Database:
# connect to database: psql -U vagrant --port 5432 -d lucedb
import os
if os.environ.get('SIMULATION') == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lucedb',
            'USER': 'luce',
            'PASSWORD': 'luce123456',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lucedb',
            'USER': 'luce',
            'PASSWORD': 'luce123456',
            'HOST': 'postgres_db',
            'PORT': '5432',
        }
    }
