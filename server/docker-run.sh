#!/bin/bash

LOGFILE_GRPC=/usr/src/app/data/log_grpc.txt
LOGFILE_WEB=/usr/src/app/data/log_web.txt

# Start the first process
PYTHONPATH=$(pwd) python3 gaia_server/server_grpc.py | rotatelogs -n 5 "${LOGFILE_GRPC}" 1M &
#PYTHONPATH=$(pwd) python3 gaia_server/server_grpc.py > "${LOGFILE_GRPC}" 2>&1 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start serve-grpc: $status"
  exit $status
fi

# Start the second process
PORT=$(cat gaia_server/constants.py | grep WEB_SERVER_PORT | cut -d "=" -f 2 | xargs)
gunicorn -w 4 -b 0.0.0.0:${PORT} --pythonpath gaia_server server_web:webserver | rotatelogs -n 5 "${LOGFILE_WEB}" 1M &
#gunicorn -w 4 -b 0.0.0.0:${PORT} --pythonpath gaia_server server_web:webserver > "${LOGFILE_WEB}" 2>&1 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start serve-web: $status"
  exit $status
fi

while sleep 60; do
  ps aux | grep serve-grpc | grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux | grep serve-web | grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."

    if [ $PROCESS_1_STATUS -ne 0 ]; then
        echo "Process 1 has already exited."
    fi
    if [ $PROCESS_2_STATUS -ne 0 ]; then
        echo "Process 2 has already exited."
    fi

    exit 1
  fi
done

