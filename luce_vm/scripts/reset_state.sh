#!/usr/bin/env bash

# Gently shutdown old processes
tmux kill-session -t "jupyter_ganache_django" 2> /dev/null

# Reset ganache back to default demo state
rm -r /home/vagrant/.ganache_db/*
cp /home/vagrant/.ganache_db_default/* /home/vagrant/.ganache_db

# Reset sqlite back to initial demo state
cp /vagrant/luce_django/luce/utils/fixtures/db_lucedb_v2.sqlite3 /vagrant/luce_django/luce/db.sqlite3 
