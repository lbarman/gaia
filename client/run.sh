#!/usr/bin/env bash

SCRIPT_NAME="gaia_client.py"
LOG_FILE_GAIA="gaia-client.txt"

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