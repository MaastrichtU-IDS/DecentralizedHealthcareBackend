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


INIT_USER_JSON="/tmp/auto_generated_user.json"
# cat > $INIT_USER_JSON <<EOF
# [
#     {
#         "model": "accounts.user",
#         "pk": 1,
#         "fields": {
#             "password": "$ADMIN_PASSWORD",
#             "last_login": null,
#             "email": "$ADMIN_EMAIL",
#             "first_name": "Admin",
#             "last_name": "User",
#             "institution": "Maastricht University",
#             "ethereum_public_key": "0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
#             "ethereum_private_key": "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3",
#             "is_approved": true,
#             "active": true,
#             "staff": true,
#             "admin": true
#         }
#     }
# ]
# EOF

cat > $INIT_USER_JSON <<EOF
[
    {
        "model": "accounts.user",
        "pk": 1,
        "fields": {
            "first_name": "user",
            "last_name": "admin",
            "email": "$ADMIN_EMAIL",
            "password": "$ADMIN_PASSWORD",
            "institution": "Maastricht University",
            "user_type": 0,
            "gender": 0,
            "country": "Netherlands",
            "ethereum_public_key": "0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
            "ethereum_private_key": "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3",
            "age": "25"
        }
    }
]
EOF

# {"first_name":"aaa","last_name":"aa","age":"23","email":"aa@aa.ss",
# "institution":"aaa","country":"aa","password":"password","gender":0,"create_wallet":true,"user_type":1}

# {'first_name': 'aa', 'last_name': 'aa', 'age': 'aa', 'email': 'aa@aa.aa', 'institution': 'aa', 'country': 'aa', 'password': 'password', 'gender': 0, 'create_wallet': True, 'user_type': 1}

cat $INIT_USER_JSON

# TODO: Preload the admin user in database
# python /app/src/luce/manage.py loaddata $INIT_USER_JSON


# python /app/src/luce/manage.py loaddata /app/src/luce/utils/fixtures/demo_users.json
# TODO: also trigger  the luce registry

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
