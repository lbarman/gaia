#!/usr/bin/env bash

SCRIPT_NAME="gaia_client.py"
LOG_FILE_GAIA="logs/gaia-client.txt"
LOG_FILE_SSH_1="logs/tunnel_ssh.txt"
LOG_FILE_SSH_2="logs/tunnel_video.txt"

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
	rm -f "$LOG_FILE_GAIA"
	nohup python2 "${SCRIPT_NAME}" 2>&1 >"$LOG_FILE_GAIA" &
else
	echo "Script ${SCRIPT_NAME} already running, not starting"
fi

# Make sure the script is not running already
ps -ux | grep "[s]sh -N -R"
isRunning=$(ps -ux | grep "[s]sh -N -R" | wc -l)
echo "$isRunning"

if [ "$isRunning" -ne 2 ]; then
    rm -f "$LOG_FILE_SSH_1"
    rm -f "$LOG_FILE_SSH_2"
    echo "Starting ssh tunnels..."
    kill $(pgrep -f "ssh -N -R")
    nohup ssh -N -R 11734:localhost:22 raspi@lbarman.ch -p 11733 2>&1 >"$LOG_FILE_SSH_1"  &
    nohup ssh -N -R 11735:localhost:8081 raspi@lbarman.ch -p 11733 2>&1 >"$LOG_FILE_SSH_2"  &
else
    echo "Ssh tunnel already started, not starting"
fi
