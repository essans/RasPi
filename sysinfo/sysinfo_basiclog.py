#!/usr/bin/env python3

#basic logging in python which can be called via crontab -e
#0,15,30,45 * * * * python3 /home/pi/code/cron/sysinfo_basiclog.py >> /home/pi/log/sysinfo.log


import subprocess

temp_cmd = 'vcgencmd measure_temp'

datetime_cmd = 'date'

temp = subprocess.check_output(temp_cmd,shell=True).decode('utf-8')

datetime = subprocess.check_output(datetime_cmd,shell=True).decode('utf-8').rstrip('\n')

print(datetime+" - "+temp,end='')
