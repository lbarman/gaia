#!/bin/bash

CLIENT_DIR=$(dirname $(pwd))
LOG_DIR="${CLIENT_DIR}/var"
TEST_FILE="${LOG_DIR}/is_inet_up"
LOG_FILE="${LOG_DIR}/reboots.log"

# Edit this function if you want to do something besides reboot
no_inet_action() {
    LAST_EDIT=$(date -r $TEST_FILE)
    echo "Still no internet connection, first test at ${LAST_EDIT}. Rebooting" > $LOG_FILE
    shutdown -r +1 'No internet.'
}

# test for internet
if nc -zw1 google.com 443; then
    echo 1 > $TEST_FILE
    (>&1 echo "Internet OK")
else
    (>&1 echo "Internet not OK")
    if [ `cat $TEST_FILE` == 0 ]; then
        no_inet_action
    else
        LAST_EDIT=$(date -r $TEST_FILE)
        echo "No internet connection, but we had it at ${LAST_EDIT}" > $LOG_FILE
    fi
    echo 0 > $TEST_FILE
fi