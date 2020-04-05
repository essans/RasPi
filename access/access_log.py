#!/usr/bin/env python3

import subprocess
import pandas as pd
import time
import re
import sys
from ipwhois import IPWhois

#extracts access info from ufw.log and auth.log.
#checks IP address for external access (or attempted access)
#query whois service for identity
#stores new records, then writes to file
#run via  crontab -e
#0,15,30,45 * * * * python3 /home/pi/code/cron/access_log.py

def src_details(ip_addr):

	src = {}

	if (ip_addr in ['None','0.0.0.0']) or (ip_addr[0:7]=='192.168'):
		src['name'] = ''
		#src['descr'] = ''
		src['cntry'] = ''
		src['city'] = ''
		#src['state'] = ''
		src['addr'] = ''
		#src['emails'] = ''

	else:

		obj = IPWhois(ip_addr)
		res = obj.lookup_whois()

		src['name'] = res['nets'][0]['name']
		#src['descr'] = res['nets'][0]['description']

		src['cntry'] = res['nets'][0]['country']
		src['city'] = res['nets'][0]['city']
		#src['state'] = res['nets'][0]['state']

		#if scr['addr'] is not None:
		#	src['addr'] = res['nets'][0]['address'].replace('\n',',')
		#else:
		#	src['addr']=''

		#src['emails'] = str(res['nets'][0]['emails'])

	return src

def to_epoch(datetime,timeformat):
	time_tuple = time.strptime(datetime,timeformat)
	time_epoch = time.mktime(time_tuple)

	return time_epoch


#load prior log file & get epoch for last lines
df_old = pd.read_csv("/home/pi/log/access.log", sep="|",header=None)

ufw_last_epoch = float(df_old[df_old.iloc[:,2]=="ufw"].iloc[-1:,0])
auth_last_epoch = float(df_old[df_old.iloc[:,2]=="sshd"].iloc[-1:,0])


#bash commands copy the log files
ufw_snapshot_cmd = 'cp /var/log/ufw.log /home/pi/log/ufw.log.tmp'
auth_snapshot_cmd = 'cp /var/log/auth.log /home/pi/log/auth.log.tmp'


#bash commands to grep required firewall log information
ufw_ip_cmd = 'grep -va AUDIT /home/pi/log/ufw.log.tmp | grep -va SRC=192. | grep -aoE "SRC=([0-9]{1,3}\.){3}[0-9]{1,3}"'
ufw_datetime_cmd = 'grep -va AUDIT /home/pi/log/ufw.log.tmp | grep -va SRC=192. | cut -d" " -f1,2,3'

#bash commands to grep required authlog information
auth_ip_cmd = 'grep -a sshd /home/pi/log/auth.log.tmp | cut -d"]" -f2,3'
auth_datetime_cmd = 'grep -a sshd /home/pi/log/auth.log.tmp | awk "{print \$1, \$2, \$3}"' 

#copy log files
subprocess.call(ufw_snapshot_cmd,shell=True)
subprocess.call(auth_snapshot_cmd,shell=True)


#execute grep command to grab ufw log info and convert to series
try:
        ufw_ip_str = pd.Series(subprocess.check_output(ufw_ip_cmd,shell=True).decode('utf-8').splitlines())
        ufw_datetime = pd.Series(subprocess.check_output(ufw_datetime_cmd,shell=True).decode('utf-8').splitlines())

        ufw_datetime = "2020 "+ufw_datetime

        ufw_epoch = ufw_datetime.apply(lambda x: to_epoch(x,"%Y %b %d %H:%M:%S"))

#return blank series in the case of an error
except subprocess.CalledProcessError:
	ufw_ip_str=pd.Series([])
	ufw_datetime=pd.Series([])
	ufw_epoch=pd.Series([])

ufw_temp = pd.concat([ufw_epoch,ufw_datetime,ufw_ip_str],axis=1).reset_index(drop=True)

#filter for new records only

ufw_temp = ufw_temp[ufw_temp.iloc[:,0]>ufw_last_epoch].reset_index(drop=True)


#execute grep command to grab auth.log and convert to series
try:
        auth_ip_str = pd.Series(subprocess.check_output(auth_ip_cmd,shell=True).decode('utf-8').splitlines())
        auth_datetime = pd.Series(subprocess.check_output(auth_datetime_cmd,shell=True).decode('utf-8').splitlines())

        auth_datetime = "2020 "+auth_datetime

        auth_epoch = auth_datetime.apply(lambda x: to_epoch(x,"%Y %b %d %H:%M:%S"))

#return blank series in the case of an errror
except subprocess.CalledProcessError:
        auth_ip_str=pd.Series([])
        auth_datetime=pd.Series([])

auth_temp = pd.concat([auth_epoch,auth_datetime,auth_ip_str],axis=1).reset_index(drop=True)

#filter for new sshd records only
auth_temp = auth_temp[auth_temp.iloc[:,0]>auth_last_epoch].reset_index(drop=True)

#datetime = subprocess.check_output(datetime_cmd,shell=True).decode('utf-8').rstrip('\n')


#extract IP address
ufw_ip = ufw_temp.iloc[:,2].apply(lambda x: re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', x).group())



#call user function to get whois details and then turn into dataframe
ufw_src = ufw_ip.apply(lambda x: src_details(x))
ufw_src_df = pd.DataFrame([x for x in ufw_src]).reset_index(drop=True)

df_ufw = pd.concat([ufw_temp,ufw_ip,ufw_src_df],axis=1,ignore_index=True)

df_ufw.insert(2,"type","ufw")

#basically do the same for auth.log
auth_ip_temp = auth_temp.iloc[:,2].apply(lambda x: re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', x))
auth_ip = auth_ip_temp.apply(lambda x: "None" if x is None else x.group())
auth_src = auth_ip.apply(lambda x: src_details(x))
auth_src_df = pd.DataFrame([x for x in auth_src]).reset_index(drop=True)

df_auth = pd.concat([auth_temp,auth_ip,auth_src_df],axis=1,ignore_index=True)

df_auth.insert(2,"type","sshd")


#now join both ufw and authlog dfs
df = pd.concat([df_auth,df_ufw],axis=0,sort=False).reset_index(drop=True)

df.sort_values(df.columns[0],inplace=True)

if df.shape[0] == 0:
	sys.exit()

df.columns = df_old.columns


df = pd.concat([df_old,df],axis=0).reset_index(drop=True)


df.to_csv("/home/pi/log/access.log", sep="|", mode = "w",header=None,index=None)
