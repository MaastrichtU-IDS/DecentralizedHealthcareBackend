#!/bin/sh -e


APP_DB_USER=vagrant
APP_DB_PASS=luce
APP_DB_NAME=lucedb
PG_VERSION=9.4
LUCEDB_IP=192.168.72.3
LUCEDB_PORT=5432

##############################
# Database Usage Information #
##############################

print_db_usage () {
  echo "Your PostgreSQL database is running"
  echo "  Host: $LUCEDB_IP"
  echo "  Port: $LUCEDB_PORT"
  echo "  Database: $APP_DB_NAME"
  echo "  Username: $APP_DB_USER"
  echo "  Password: $APP_DB_PASS"
  echo ""
  echo 
  echo "postgresql://$APP_DB_USER:$APP_DB_PASS@$LUCEDB_IP:$LUCEDB_PORT/$APP_DB_NAME"
  echo ""
  echo 
  echo "To access the database via psql:"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h $LUCEDB_IP -p $LUCEDB_PORT $APP_DB_NAME"
}

print_db_usage


