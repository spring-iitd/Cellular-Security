#!/bin/bash

# Define your session name
SESSION_NAME="vagrant"

# Start a new tmux session in detached mode
tmux new-session -d -s $SESSION_NAME

# Array of commands to run in separate tmux windows
commands=(
    "vagrant up core_nw"
    "vagrant up ran_nw_1"
    "vagrant up ran_nw_2"
    "vagrant up ran_nw_3"
    "vagrant up ran_nw_4"
    "vagrant up ran_nw_5"
    "vagrant up ran_nw_6"
    "vagrant up ran_nw_7"
    "vagrant up ran_nw_8"
    "vagrant up ran_nw_9"
    "vagrant up ran_nw_0"
    "vagrant up ue_nw"
)

# Loop through commands and create a new window for each
for cmd in "${commands[@]}"; do
    tmux new-window -t $SESSION_NAME -n "$(echo $cmd | awk '{print $3}')" "$cmd"
done

# Attach to the session
tmux attach -t $SESSION_NAME
