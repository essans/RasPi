#!/usr/bin/env python3

import sys
import argparse

from fabric import Connection

parser = argparse.ArgumentParser(description="execute command across cluster")

parser.add_argument('-v',
        required=False,
        type=str,
        default='Y',
        help="Verbose (default: Y)")

parser.add_argument('-c',
	required=False,
	type=str,
	default='echo $(hostname), $(hostname -I)',
	help="command to execute (default: 'hostname -I')")

parser.add_argument('-m',
	required=False,
	type=str,
	default='N',
	help='include master node (default:  N)')


parser.add_argument('-n',
        required=False,
        type=int,
        default=99,
        help='node number (default: 99 for all)')


args = parser.parse_args()


hosts = [
        '192.168.5.41', #1
        '192.168.5.42', #2
        '192.168.5.19', #3
        '192.168.5.8', #4
        '192.168.5.9' #5
]

master = '192.168.5.1'

user   = ''

password = ''

m_password = ''


if args.m in ['Y','y']:

	if args.v in ['Y','y']:
		print('\n >>> ATTEMPTING MASTER \n')

	try:
		c = Connection(master,user=user,connect_kwargs={"password": m_password})
		result = c.run(args.c)

	except:
		print('Problem with master node \n')


if args.n !=99:

	if args.v in ['Y','y']:
                print('\n >>> ATTEMPTING NODE: '+str(args.n)+'\n')

	try:
		c = Connection(hosts[args.n-1],user=user,connect_kwargs={"password": password})
		result = c.run(args.c)

	except:
		print("Problem with node "+str(args.n)+'\n')

	sys.exit()	



for node,host in enumerate(hosts):

	if args.v in ['Y','y']:
                print('\n >>> ATTEMPTING NODE: '+str(node+1)+'\n')

	try:
		c = Connection(host,user=user,connect_kwargs={"password": password})

		result = c.run(args.c)

	except:
		print("Problem with node "+str(node+1)+'\n')
