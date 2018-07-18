#!/usr/bin/env bash

isRunning=$(ps -u | grep "[p]ython2 raspberry-run.py" | wc -l)

if [ "$isRunning" -ne 1 ]; then
	pkill python
	pkill python2
	echo "Starting script..."
	rm -rf log.txt &
	nohup python2 raspberry-run.py 2>&1 >log.txt &
else
	echo "Script already running, not starting"
fi
