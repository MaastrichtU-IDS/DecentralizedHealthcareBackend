#!/usr/bin/env bash
# This script starts the jupyter and ganache server processes in the background

# Gently shutdown old processes
tmux kill-session -t "jupyter_ganache_django" 2> /dev/null

# Create detached tmux session from terminal
tmux new-session -d -s jupyter_ganache_django
tmux rename-window 'jupyter_ganache_django'

# Send in commands to start Jupyter Server
tmux send-keys -t jupyter_ganache_django.0 'eval "$(conda shell.bash hook)"' ENTER
tmux send-keys -t jupyter_ganache_django.0 'conda activate luce_vm' ENTER
tmux send-keys -t jupyter_ganache_django.0 'jupyter notebook --no-browser --ip 0.0.0.0 --notebook-dir=/vagrant/jupyter/' ENTER

# Select first window in session and split it
tmux select-window -t jupyter_ganache_django:0
tmux split-window -v

# Send in commands to start Ganache Server
tmux send-keys -t jupyter_ganache_django.1 'eval "$(conda shell.bash hook)"' ENTER
tmux send-keys -t jupyter_ganache_django.1 'conda activate luce_vm' ENTER
tmux send-keys -t jupyter_ganache_django.1 'ganache-cli --mnemonic luce --db ~/.ganache_db --networkId 72 --host 0.0.0.0 --accounts 3 --defaultBalanceEther 1000000 -l 80000000000' ENTER

# Split window once again
tmux split-window -v

# Send in commands to start Django Server
tmux send-keys -t jupyter_ganache_django.2 'eval "$(conda shell.bash hook)"' ENTER
tmux send-keys -t jupyter_ganache_django.2 'conda activate luce_vm' ENTER
tmux send-keys -t jupyter_ganache_django.2 'pip install -r /vagrant/luce_django/luce/requirements.txt' ENTER
tmux send-keys -t jupyter_ganache_django.2 'python /vagrant/luce_django/luce/manage.py migrate' ENTER
tmux send-keys -t jupyter_ganache_django.2 'python /vagrant/luce_django/luce/manage.py runserver 0.0.0.0:8000 --noreload' ENTER



echo
printf "The Jupyter, Ganache and Django servers have been started..\n\n"

printf "Visit http://127.0.0.1:8888 to access the Jupyter 
notebook environment. The password is: luce\n"
echo

printf "Visit http://127.0.0.1:8000 to access the 
Luce Data Exchange.
Demo accounts: 
provider@luce.com   | provider
requester@luce.com  | requester
\n"
echo


# Attach session for quick debugging
#tmux attach-session -t jupyter_ganache_django

# The following resource helped me greatly in getting this script to work:
# https://stackoverflow.com/questions/5447278/bash-scripts-with-tmux-to-launch-a-4-paned-window
