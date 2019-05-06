#!/bin/bash

function restart(){
    pkill ffmpeg
    nohup /usr/local/bin/ffmpeg -loglevel panic -framerate 10 -video_size 1280x720 -i /dev/video0 -vsync 1 -c:v h264_omx -b:v 1024k -maxrate 1024k -bufsize 1024k -g 30 -pix_fmt yuv420p -framerate 15 -f flv rtmp://live.twitch.tv/app/live_424693626_cieaTZWRlvLuHdWydKh3cdRfxjHeYh 2>&1 >/dev/null &
}

psRunning=$(px cax | grep ffmpeg | wc -l)
twichReceiving=$(curl -sH 'Client-ID: d24enqloigmpwyz3qop2c9gn6tioqg' -X GET 'https://api.twitch.tv/helix/streams?user_login=gasparovcam' | jq '.data?[0]' | wc -l)

if [ $psRunning -eq 0 ]; then
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Process not running, restarting stream..."
    restart
elif [ $twitchReceiving -eq ]
then
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Twitch not receiving, restarting stream..."
    restart
else
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Process already running, all good."
fi
