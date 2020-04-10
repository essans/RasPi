#!/bin/bash

#Execute via crontab -e
#0,15,30,45 * * * * bash /home/pi/code/bash/sysinfo_logger.sh >> /home/pi/log/$(uname -n)_sysinfo.log


#sysinfo_attr=$(/home/pi/code/bash/sysinfo.sh | awk '{print $1}' | tr -d "=" | sed 's/SYSTEM_INFORMATION//g' | sed 's/   //g')

sysinfo=$(/home/pi/code/bash/sysinfo.sh)

sysinfo_attr=$(echo "$sysinfo" | awk '{print $1}' | tr -d "=" | sed 's/SYSTEM_INFORMATION//g' | sed 's/   //g')


#echo $sysinfo

attributes=$(echo $sysinfo_attr)

headertosave=""
recordtosave=""

quote="\""

for attr in $attributes
do
	headertosave+="${attr},"


	value=$(echo "$sysinfo" | awk "/(^$attr)/" | awk '{$1="";print $0}')

	value=${value:1}

	kv_pair="$quote${attr}$quote:$quote${value}$quote"

	recordtosave+="${kv_pair}, "


done

headertosave=${headertosave::-1}

recordtosave=${recordtosave::-2}

echo "{$recordtosave}" 
