#!/bin/bash

TEST_FILE="/tmp/is_inet_up"

# test for internet
if nc -zw1 google.com 443; then
    echo 1 > ${TEST_FILE}
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Internet OK."
else
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Internet not OK."
    if [ `cat ${TEST_FILE}` == 0 ]; then
        LAST_EDIT=$(date -r ${TEST_FILE})
        echo "[`date +"%d-%m-%Y %H:%M:%S"`] Still no internet connection, previous test at ${LAST_EDIT}. Rebooting."
        shutdown -r +1 'No internet.'
    else
        LAST_EDIT=$(date -r ${TEST_FILE})
        echo "[`date +"%d-%m-%Y %H:%M:%S"`] No internet connection, but we had it at ${LAST_EDIT}. Trying once more."
    fi
    echo 0 > "${TEST_FILE}"
fi