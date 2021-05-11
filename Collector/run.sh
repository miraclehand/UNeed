#!/bin/bash

cpucore=`grep -c processor /proc/cpuinfo`
let workers=$cpucore*2

cd back_end
/usr/local/bin/gunicorn --workers $workers --bind 0.0.0.0:8000 --access-logfile log/access.log --error-logfile log/error.log server:app --preload
