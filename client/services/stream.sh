#!/bin/sh -
pkill ffmpeg
rm -f /tmp/stream.log
FFREPORT="level=32:file=/tmp/stream.log" /usr/local/bin/ffmpeg -loglevel panic -framerate 10 -video_size 1280x720 -i /dev/video0 -vsync 1 -c:v h264_omx -b:v 1024k -maxrate 1024k -bufsize 1024k -g 30 -pix_fmt yuv420p -framerate 15 -f flv rtmp://live.twitch.tv/app/live_424693626_cieaTZWRlvLuHdWydKh3cdRfxjHeYh