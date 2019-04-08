#!/bin/bash

# always refer to CWD
cd "$(dirname "$0")"

CLIENT_DIR=$(dirname $(pwd))
LOG_DIR="${CLIENT_DIR}/var"
TEST_FILE="${LOG_DIR}/is_inet_up"
LOG_FILE="${LOG_DIR}/reboots.log"

# test for internet
if nc -zw1 google.com 443; then
    echo 1 > $TEST_FILE
    echo "Internet OK."
    echo "Internet OK." > $LOG_FILE
else
    echo "Internet not OK."
    if [ `cat $TEST_FILE` == 0 ]; then
        LAST_EDIT=$(date -r $TEST_FILE)
        echo "Still no internet connection, previous test at ${LAST_EDIT}. Rebooting."
        echo "Still no internet connection, previous test at ${LAST_EDIT}. Rebooting." >> $LOG_FILE
        shutdown -r +1 'No internet.'
    else
        LAST_EDIT=$(date -r $TEST_FILE)
        echo "No internet connection, but we had it at ${LAST_EDIT}. Trying once more."
        echo "No internet connection, but we had it at ${LAST_EDIT}. Trying once more." >> $LOG_FILE
    fi
    echo 0 > $TEST_FILE
fi