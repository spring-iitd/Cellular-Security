#!/bin/bash

# Get the list of process IDs (PIDs) of processes matching 'open5gs' and remove duplicates
PIDS=$(sudo netstat -tulpn | grep -E 'open5gs' | awk '{print $7}' | awk -F'/' '{print $1}' | awk '!x[$0]++')
PID=$(sudo netstat -tulpn | grep -E 'open5gs-sgwud' | awk '{print $6}' | awk -F'/' '{print $1}' | awk '!x[$0]++')

echo "Lisiting all the PID corresponding to open5gs"
echo $PIDS
echo $PID
echo "Kill all the process with above mentioned PID"
# Loop through each PID and kill the corresponding process
for P in $PIDS; do
    kill -9 $P
done

for P in $PID; do
    kill -9 $P
done

echo "All processes matching 'open5gs' have been killed."
