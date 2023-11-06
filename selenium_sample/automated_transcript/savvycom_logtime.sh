#!/bin/sh

# crontab -e
# 0 * * * * /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime.sh
# NOTE: this script is running in castnet-dev

xvfb-run --listen-tcp --server-num 44 \
    --auth-file /tmp/xvfb.auth \
    -s "-ac -screen 0 1920x1080x24" \
    /home/xuananh/repo/python-note/.venv/bin/python \
    /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime.py &

export DISPLAY=:44
mkdir -p /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime-video
ffmpeg -f x11grab -video_size 1920x1080 -i :44 -codec:v libx264 -r 12 \
    /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime-video/$(date +'%Y-%m-%d__%H-%M-%S').mp4