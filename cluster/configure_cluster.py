#!/usr/bin/env python3

#useful script for executing commands across cluster with option of including the master 
#
#./cluster_config.py --help
#optional arguments:
#  -h, --help show this help message and exit
#  -c         command to execute (default is to print hostnames)
#  -m         include master node (Y/N)

import sys
import argparse
from fabric import Connection

parser = argparse.ArgumentParser(description="execute command across cluster")

parser.add_argument('-c',
        required=False,
        type=str,
        default='echo $(hostname), $(hostname -I)',
        help='command to execute')

parser.add_argument('-m',
        required=False,
        type=str,
        default='N',
        help='include master node (Y/N)')

args = parser.parse_args()

hosts = [
        'xxx.xxx.xxx.xxx',
        'xxx.xxx.xxx.xxx',
        'xxx.xxx.xxx.xxx',
        'xxx.xxx.xxx.xxx', 
        'xxx.xxx.xxx.xxx' 
]

master = 'xxx.xxx.xxx.xxx'

user   = "pi"

password = ""
m_password = ''  #master


if args.m in ['Y','y']:

	try:
		c = Connection(master,user=user,connect_kwargs={"password": m_password})
		result = c.run(args.c)

	except:
		print("Problem with master node")

                
for host in hosts:

	try:
		c = Connection(host,user=user,connect_kwargs={"password": password})
		result = c.run(args.c)

	except:
		print("Problem with "+host)
  
