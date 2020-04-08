#!/bin/bash

# measure and display temp of system-on-chip temp every 5 seconds


printf "%-10s | %5s\n" "TIMESTAMP" "TEMP(degC)"
printf "%15s\n" "-----------------------"

while true
do
        
        temp=$(vcgencmd measure_temp | grep -o '[0-9]*\.[0-9]*')
        timestamp=$(date +'%s')
        printf "%-10s | %5s\n" "$timestamp" "$temp"
        sleep 5

done
