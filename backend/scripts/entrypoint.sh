#!/bin/bash

# Docker entrypoint

# conda init bash
# conda activate luce_vm

### WAITING POSTGRES START ###
RETRIES=1000
while [ "$RETRIES" -gt 0 ]
do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  PG_STATUS="$(pg_isready -h postgres_db -U $POSTGRES_USER)"
  PG_EXIT=$(echo $?)
  echo "Postgres Status: $PG_EXIT - $PG_STATUS"
  if [ "$PG_EXIT" = "0" ];
    then
      RETRIES=0
  fi
  sleep 5  # timeout for new loop
done

# Prepare Django
python /app/src/luce/manage.py makemigrations accounts # TODO: I am not sure why the migration of accounts can't be executed automatically
python /app/src/luce/manage.py migrate


# # Preload 3 hardcoded users in database
# python /app/src/luce/manage.py loaddata /app/src/luce/utils/fixtures/demo_users.json
# # Preload in demo datasets: 7 datasets (5 published, 2 unpublished)
# python /app/src/luce/manage.py loaddata /app/src/luce/utils/fixtures/demo_data.json


## OR Create users based on GanacheDB
## Create superuser (if no users in init JSON)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('vagrant@luce.com','Vagrant','Luce','Maastricht University','vagrant')" | python /luce/src/luce_django/luce/manage.py shell


# echo "👤 Demo accounts:"
# echo "provider@luce.com   | provider"
# echo "requester@luce.com  | requester"

# python /app/scripts/init_luce_registry.py


echo "🚀 Access the LUCE backend API on http://localhost:8000"


# Start Django on port 8000
python /app/src/luce/manage.py runserver 0.0.0.0:8000

# curl -H "Authorization: XXX" -H "Content-Type: application/json" -X POST http://localhost8000/admin/deployRegistry
