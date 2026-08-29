#!/bin/bash

# Extract the PID of the first matching Python process, hopefully ZenPlayer
PID=$(ps -e | grep python | grep -v grep | head -n 1 | awk '{print $1}')

# Check if a PID was found
if [ -z "$PID" ]; then
    echo "No matching Python process found."
    exit 1
fi

echo "Found Python process with PID: $PID"
echo "Requesting sudoi previlege to elevate niceness and I/O scheduling class..."

sudo renice -n -5 -p "$PID"
sudo ionice -c 1 -n 3 -p "$PID"

echo "Process details after changes:"
ps -o pid,comm,ni,cls -p "$PID"

