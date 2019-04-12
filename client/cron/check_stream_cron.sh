#!/bin/bash

if [ `ps cax | grep ffmpeg | wc -l` -eq 0 ]; then
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Restarting stream..."
    pkill ffmpeg
    /usr/local/bin/ffmpeg -loglevel panic -framerate 10 -video_size 1280x720 -i /dev/video0 -vsync 1 -c:v h264_omx -b:v 1024k -maxrate 1024k -bufsize 1024k -g 30 -pix_fmt yuv420p -framerate 15 -f flv rtmp://live.twitch.tv/app/live_424693626_cieaTZWRlvLuHdWydKh3cdRfxjHeYh 2>&1 >/dev/null &
else
    echo "[`date +"%d-%m-%Y %H:%M:%S"`] Process already running, all good."
fi
