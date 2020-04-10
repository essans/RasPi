#!/bin/bash

HOST='raspi.soobratty.com'
USER='raspi'
PASSWORD=''

cd /home/pi/log

prev_sysinfo_dump=`cat /home/pi/log/sysinfodump.ftp`
current_sysinfo_dump=`ls -ltr /home/pi/log/sysinfo.dump`

prev_sysinfo_log=`cat /home/pi/log/sysinfo.ftp`
current_sysinfo_log=`ls -ltr /home/pi/log/sysinfo.log`

prev_access_log=`cat /home/pi/log/accesslog.ftp`
current_access_log=`ls -ltr /home/pi/log/access.log`



if [ "$prev_sysinfo_dump"  != "$current_sysinfo_dump" ]; then
        curl -T /home/pi/log/sysinfo.dump -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com/
        ls -ltr /home/pi/log/sysinfo.dump > sysinfodump.ftp
fi



if [ "$prev_sysinfo_log"  != "$current_sysinfo_log" ]; then
	curl -T /home/pi/log/sysinfo.log -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com/
	ls -ltr /home/pi/log/sysinfo.log > sysinfo.ftp
fi



if [ "$prev_access_log" != "$current_access_log" ]; then
	curl -T /home/pi/log/access.log -u $USER:$PASSWORD ftp://ftp.raspi.soobratty.com
	ls -ltr /home/pi/log/access.log > accesslog.ftp
fi
