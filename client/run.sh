#!/usr/bin/env bash

SCRIPT_NAME="gaia_client.py"
LOG_FILE="logs/gaia-client.txt"
LOG_FILE_SSH="logs/tunnel.txt"

# Always run stuff relative to this very folder, even when calling ./xxx/yyy/folder/gaia/client/run.sh
cd "$(dirname "$0")"

# Make sure the script is not running already
ps -ux | grep "[p]ython2 ${SCRIPT_NAME}"
isRunning=$(ps -ux | grep "[p]ython2 ${SCRIPT_NAME}" | wc -l)
echo "$isRunning"

if [ "$isRunning" -ne 1 ]; then
	pkill python
	pkill python2
	echo "Starting script ${SCRIPT_NAME}..."
	rm -rf "$LOG_FILE"
	nohup python2 "${SCRIPT_NAME}" 2>&1 >"$LOG_FILE" &
else
	echo "Script ${SCRIPT_NAME} already running, not starting"
fi

# Make sure the script is not running already
ps -ux | grep "[s]sh -N -R"
isRunning=$(ps -ux | grep "[s]sh -N -R" | wc -l)
echo "$isRunning"

if [ "$isRunning" -ne 1 ]; then
    echo "Starting ssh tunnel..."
    nohup ssh -N -R 11734:localhost:22 root@lbarman.ch -p 11733 2>&1 >"$LOG_FILE_SSH"  &
else
    echo "Ssh tunnel already started, not starting"
fi