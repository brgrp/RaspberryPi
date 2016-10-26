#!/bin/bash
# Please install nc on debian

PORT=2222

clear

echo "Start RaspberryPi camera image transmitter....."

if [ -n "$1" ]; then echo "Set port to $1"; PORT=$1; fi

read IP_ADDR <<< `ifconfig eth0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`

echo "Send data... $IP_ADDR:$PORT!"
raspivid -t 0 -w 1280 -h 720 -hf -ih -fps 30 -o - | nc -k -l -p $PORT
