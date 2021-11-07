#!/usr/bin/env bash
# This script provides a convenient interface to interact with the LUCE servers
# This script is placed in the default shell path so it can be directly executed as a command

# No arguments
if [ $ == ]
then
	printf "Please use luce with one of the following arguments:
	luce start  ->  Starts the Jupyter, Ganache and Django servers
	luce stop   ->  Stops all running servers

	luce status ->  Show the current status of the servers [running/not running]
	luce reset  ->  Reset blockchain and default database back to demo state

	luce start_psql  ->  Starts servers and uses alternative PSQL database

	Note: To use Django with PostgreSQL please ensure the lucedb vm is running, 
	otherwise the Luce Data Exchange will not be accessible. To start lucedb:
	$ vagrant up lucedb
	\n"
	echo
	exit
fi

# Luce start
if [ $ == ]
then
	bash /home/vagrant/start_servers.sh
	exit
fi


# Luce stop
if [ $ == ]
then
	bash /home/vagrant/stop_servers.sh
	exit
fi

# luce_psql
if [ $ == ]
then
	bash /home/vagrant/start_servers_psql.sh
	exit
fi

# luce reset
if [ $ == ]
then
	bash /home/vagrant/reset_state.sh
	exit
fi

if [ $ == ]
then
	# Wrong arguments
	echo "Unknown argument: $ "
	printf "Please use luce with one of the following arguments:
	luce start  ->  Starts the Jupyter, Ganache and Django servers
	luce stop   ->  Stops all running servers

	luce start_psql  ->  Starts servers and uses alternative PSQL database

	Note: To use Django with PostgreSQL please ensure the lucedb vm is running, 
	otherwise the Luce Data Exchange will not be accessible. To start lucedb:
	$ vagrant up lucedb
	\n"
	echo
fi

