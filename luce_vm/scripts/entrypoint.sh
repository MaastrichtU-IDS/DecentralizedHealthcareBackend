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

# Start Ganache on port 8545 with hardcoded accounts for provider/requester
# nohup ganache-cli --mnemonic luce --db ~/.ganache_db --networkId 72 --host 0.0.0.0 --accounts 10 --defaultBalanceEther 1000000 --account "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3,1000000000000000000000000" --account "0xad740a17686169082f3148dcec143e4730fc69a636d710cb8e4e23ef966feadd,1000000000000000000000000" --account "0xdd11160def74259a8cfcb0282702ab65c1388cf4e0265f567fe0a3707957d810,1000000000000000000000000" &

# To output public/private keys in /ganache-keys.json
#nohup ganache-cli --mnemonic luce --db ~/.ganache_db --networkId 72 --host 0.0.0.0 --accounts 3 --defaultBalanceEther 1000000 --account_keys_path /ganache-keys.json &
# The run create_user() with those private/public keys from the JSON


## Prepare Django
python /luce/luce_vm/luce_django/luce/manage.py makemigrations accounts # TODO: I am not sure why the migration of accounts can't be executed automatically
python /luce/luce_vm/luce_django/luce/manage.py migrate

## Prepare brownie
# brownie networks add LUCE luce host=https://127.0.0.1:8545 chainid=5777
# Load 3 hardcoded users in database
# python /luce/src/luce_django/luce/manage.py loaddata /luce/src/luce_django/luce/utils/fixtures/demo_users.json
# Load in demo data: 3 users, 7 datasets (5 published, 2 unpublished)
# Load hardcoded user data, with hardcoded Ganache private keys, which will probably not match the new one generated by Ganache
# python /luce/src/luce_django/luce/manage.py loaddata /luce/src/luce_django/luce/utils/fixtures/demo_all_v2.json

## OR Create users based on GanacheDB
## Create superuser (if no users in init JSON)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('vagrant@luce.com','Vagrant','Luce','Maastricht University','vagrant')" | python /luce/src/luce_django/luce/manage.py shell
# python /luce/src/luce_django/luce/manage.py loaddata /luce/src/luce_django/luce/utils/fixtures/demo_all_v3.json
# python scripts/create_users.py


echo "👤 Demo accounts:"
echo "provider@luce.com   | provider"
echo "requester@luce.com  | requester"

echo "🚀 Access the LUCE user interface on http://localhost:8000"


# Start Django on port 8000
python /luce/luce_vm/luce_django/luce/manage.py runserver 0.0.0.0:8000


# Send in commands to start Ethereum private testnet on port 8544
#nohup geth --identity node1 --networkid 4224 --mine --miner.threads 1 --datadir "/luce/ethtestnet/node1" --nodiscover --rpc --rpcport "8544" --port "30302" --rpccorsdomain "*" --nat "any" --rpcapi admin,miner,eth,web3,personal,net --allow-insecure-unlock --password /luce/ethtestnet/node1/password.sec --ipcpath "~/.ethereum/geth.ipc" &

# Start JupyterLab server on port 8888
# exec jupyter lab --allow-root --no-browser --ip 0.0.0.0 --notebook-dir=/luce/jupyter/