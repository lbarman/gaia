#!/bin/bash

twitchReceiving="$(/usr/bin/curl -sH 'Client-ID: d24enqloigmpwyz3qop2c9gn6tioqg' -X GET 'https://api.twitch.tv/helix/streams?user_login=gasparovcam' | /usr/bin/jq '.data?[0]' | /usr/bin/wc -l)"

if [[ $twitchReceiving -le 1 ]]; then
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Twitch not receiving, restarting stream..."
    echo "************************************************************************"
    systemctl status stream.service
    systemctl stop stream.service
    sleep 5
    systemctl start stream.service
    sleep 5
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Done restarting..."
    systemctl status stream.service
    echo "************************************************************************"
else
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Twitch receiving, all good."
fi
