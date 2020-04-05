#!/bin/bash

#uploads changes to logs to ftp
#runs via cron:
#2,17,32,47 * * * * sh /home/pi/code/cron/upload_logs_to_ftp.sh


HOST='ftp://ftp.raspi.soobratty.com'
USER='user'
PASSWORD='password'

cd /home/pi/log

prev_sysinfo_log = `cat /home/pi/log/sysinfo.ftp`
current_sysinfo_log = `ls -ltr /home/pi/log/sysinfo.log`

prev_access_log = `cat /home/pi/log/accesslog.ftp`
current_access_log = `ls -ltr /home/pi/log/access.log`


if [ "$prev_sysinfo_log"  != "$current_sysinfo_log" ]; then
	curl -T /home/pi/log/sysinfo.log -u $USER:$PASSWORD $HOST
	ls -ltr /home/pi/log/sysinfo.log > sysinfo.ftp
fi


if [ "$prev_access_log" != "$current_access_log" ]; then
	curl -T /home/pi/log/access.log -u $USER:$PASSWORD $HOST
	ls -ltr /home/pi/log/access.log > accesslog.ftp
fi
