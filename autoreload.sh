#!/bin/bash

old_size=0
while true
do
sleep 1
old_size=$curr_size
curr_size=`du -bs . | awk '{print $1}'`

#echo "old: $old_size"
#echo "curr: $curr_size"

if (( curr_size != old_size ))
    then
        pkill -f "python3"
        
#        tput bel
        python3 run.py &
fi
done
