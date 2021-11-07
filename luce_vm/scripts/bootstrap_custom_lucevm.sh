#!/usr/bin/env bash

# Clean up old scripts
rm /home/vagrant/*.sh
# Copy scripts to vagrant home directory
cp /vagrant/scripts/* /home/vagrant

# Reset sqlite back to initial demo state
cp /vagrant/luce_django/luce/utils/fixtures/db_lucedb_v2.sqlite3 /vagrant/luce_django/luce/db.sqlite3 