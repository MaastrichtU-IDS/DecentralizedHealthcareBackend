#!/usr/bin/env bash
# This script starts the jupyter and ganache server processes in the background

# Gently shutdown old processes
tmux kill-server 2> /dev/null

echo
printf "All servers running on LuceVM have been stopped\n\n"
echo
