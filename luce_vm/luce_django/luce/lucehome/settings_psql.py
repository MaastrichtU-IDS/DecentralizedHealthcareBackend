# Include the following the script to use the psql server:
# export DJANGO_USE_PSQL=true
# This will override the DATABASES variable in settings.py

# Use Postgresql Database:
#connect to database: psql -U vagrant --port 5432 -d lucedb
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lucedb',
        'USER': 'vagrant',
        'PASSWORD': 'luce',
        'HOST': 'postgres_db',
        'PORT': '5432',
    }
}
