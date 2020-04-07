!/bin/bash 

#sysinfo_attr=$(/home/pi/code/bash/sysinfo.sh | awk '{print $1}' | tr -d "=" | sed 's/SYSTEM_INFORMATION//g' | sed 's/   //g')

sysinfo=$(/home/pi/code/bash/sysinfo.sh)

sysinfo_attr=$(echo "$sysinfo" | awk '{print $1}' | tr -d "=" | sed 's/SYSTEM_INFORMATION//g' | sed 's/   //g')


#echo $sysinfo

attributes=$(echo $sysinfo_attr)

headertosave=""
recordtosave=""


sep=","

for attr in $attributes
do
        headertosave+="${attr},"

        value=$(echo "$sysinfo" | awk "/(^$attr)/" | awk '{$1="";print $0}')


        recordtosave+="${value},"

done

headertosave=${headertosave::-1}

recordtosave=${recordtosave::-1}

