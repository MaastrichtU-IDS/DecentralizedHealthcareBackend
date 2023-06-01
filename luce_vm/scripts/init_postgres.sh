#!/bin/bash
set -e

# Init the posgresql DB
# Create the database user and the database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create the database user:
    CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';

    -- Create the database:
    CREATE DATABASE $POSTGRES_DB WITH OWNER=$POSTGRES_USER
                                    LC_COLLATE='en_US.utf8'
                                    LC_CTYPE='en_US.utf8'
                                    ENCODING='UTF8'
                                    TEMPLATE=template0;
EOSQL


# cat << EOF | su - postgres -c psql
# -- Create the database user:
# CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';

# -- Create the database:
# CREATE DATABASE $POSTGRES_DB WITH OWNER=$POSTGRES_USER
#                                   LC_COLLATE='en_US.utf8'
#                                   LC_CTYPE='en_US.utf8'
#                                   ENCODING='UTF8'
#                                   TEMPLATE=template0;
# EOF
