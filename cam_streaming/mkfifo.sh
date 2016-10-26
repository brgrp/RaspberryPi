#!/bin/bash

pipe=/tmp/picamfifo.500

trap "rm -f $pipe" EXIT

if [[ ! -p $pipe ]]; then
    sudo mkfifo $pipe
fi

echo "Fifo created."
