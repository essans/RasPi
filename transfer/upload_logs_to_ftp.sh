#!/bin/bash

HOST='raspi.soobratty.com'
USER='raspi'
PASSWORD='N)RBtv{Qh@B8'

uname=`hostname -s`

cd /home/pi/log

prev_sysinfo_dump=`cat /home/pi/log/$uname"_sysinfodump.ftp"`

current_sysinfo_dump=`ls -ltr /home/pi/log/$uname"_sysinfo.dump"`

prev_sysinfo_log=`cat /home/pi/log/$uname"_sysinfo.ftp"`
current_sysinfo_log=`ls -ltr /home/pi/log/$uname"_sysinfo.log"`

prev_access_log=`cat /home/pi/log/$uname"_accesslog.ftp"`
current_access_log=`ls -ltr /home/pi/log/$uname"_access.log"`



if [ "$prev_sysinfo_dump"  != "$current_sysinfo_dump" ]; then
        curl -T /home/pi/log/$uname"_sysinfo.dump" -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com/
        ls -ltr /home/pi/log/$uname"_sysinfo.dump" > $uname"_sysinfodump.ftp"
fi



if [ "$prev_sysinfo_log"  != "$current_sysinfo_log" ]; then
	curl -T /home/pi/log/$uname"_sysinfo.log" -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com/
	ls -ltr /home/pi/log/$uname"_sysinfo.log" > $uname"_sysinfo.ftp"
fi



if [ "$prev_access_log" != "$current_access_log" ]; then
	curl -T /home/pi/log/$uname"_access.log" -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com
	ls -ltr /home/pi/log/$uname"_access.log" > $uname"_accesslog.ftp"
fi
