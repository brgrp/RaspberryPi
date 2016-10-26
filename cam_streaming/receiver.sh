#!/bin/bash
# Please install netcat-traditional mplayer on debian

PORT=2222

clear

echo "Start RaspberryPi camera image receiver....."

if [ -z "$1" ]; then echo "Transmitters address [raspberrypi] NOT set... exit..."; exit 1; fi
if [ -n "$2" ]; then echo "Set port to $2"; PORT=$2; fi
read IP_ADDR <<< `ifconfig eth0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`

mplayer -fps 200 -demuxer h264es ffmpeg://tcp://$1:2222