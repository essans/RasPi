#!/usr/bin/env python3

#Tranfer files from master node to 1 or all worker nodes

#This version uses passwords so assumes cluster is sufficiently isolated/secure on the network

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description="copy files to nodes")

parser.add_argument('-v',
        required=False,
        type=str,
        default='Y',
        help="Verbose (default: Y)")


parser.add_argument('-f',
	required=True,
	type=str,
	help="file to copy")


parser.add_argument('-d',
        required=False,
        type=str,
        help="destination (default: ~/")


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

if args.n !=99:

	if args.v in ['Y','y']:
                print('\n >>> ATTEMPTING NODE: '+str(args.n)+'\n')

	try:
		xfer_cmd = 'sshpass -p ' + password + ' scp ' + args.f + ' ' + user + '@' + hosts[args.n-1] + ':' + args.d

		subprocess.call(xfer_cmd, shell=True)

	except:
		print("Problem with node "+str(args.n)+'\n')

	sys.exit()



for node,host in enumerate(hosts):

	if args.v in ['Y','y']:
                print('\n >>> ATTEMPTING NODE: '+str(node+1)+'\n')

	try:

		xfer_cmd = 'sshpass -p ' + password + ' scp ' + args.f + ' ' + user + '@' + host + ':' + args.d

		subprocess.call(xfer_cmd, shell=True)

	except:
		print("Problem with node "+str(node+1)+'\n')
