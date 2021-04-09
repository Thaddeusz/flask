#!/bin/bash

old_size=0
while true
do
sleep 1
old_size=$curr_size
curr_size=`du -bs . | awk '{print $1}'`

if (( curr_size != old_size ))
    then
        echo "**********************************"
        pkill -f "python3"
        python3 run.py &
fi
done
