#!/bin/bash

sysinfo=$(/home/pi/code/bash/sysinfo.sh)

sysinfo_attr=$(echo "$sysinfo" | awk '{print $1}' | tr -d "=" | sed 's/SYSTEM_INFORMATION//g' | sed 's/   //g')


attributes=$(echo $sysinfo_attr)

headertosave=""
recordtosave=""


for attr in $attributes
do
        headertosave+="${attr},"

        value=$(echo "$sysinfo" | awk "/(^$attr)/" | awk '{$1="";print $0}')

        recordtosave+="${value},"

done

echo "$headertosave"

echo "$recordtosave"
