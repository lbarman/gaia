#!/usr/bin/env bash

LOG_FILE_GAIA="/var/log/gaia/gaia.log"

# Always run stuff relative to this very folder, even when calling ./xxx/yyy/folder/gaia/client/run.sh
cd "$(dirname "$0")"

if [ `ps ax | grep "[p]ython3 gaia_entrypoint.py" | wc -l` -ne 1 ]; then
	pkill python
    pkill python3
	echo "[`date +"%d-%m-%Y %H:%M:%S"`] Starting script ${SCRIPT_NAME}..."
    cd python && nohup python3 gaia_entrypoint.py 2>&1 | rotatelogs -n 5 "${LOG_FILE_GAIA}" 1M &
else
	echo "[`date +"%d-%m-%Y %H:%M:%S"`] Script ${SCRIPT_NAME} already running, not starting"
fi