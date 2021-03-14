#!/usr/bin/env python3

import sys
import subprocess
import argparse

from fabric import Connection

parser = argparse.ArgumentParser(description="execute command in parallel across worker nodes")

parser.add_argument('-v',
        required=False,
        type=str,
        default='Y',
        help="Verbose (default: Y)")


parser.add_argument('-o',
        required=False,
        type=str,
        default='Y',
        help="show output (default: Y)")


parser.add_argument('-c',
	required=False,
	type=str,
	default='hostname',
	help="command to execute (default: 'hostname -I')")


parser.add_argument('-m',
	required=False,
	type=str,
	default='N',
	help='include master node (default:  N)')


parser.add_argument('-n',
        required=False,
        nargs='*',
        type=int,
        default=99,
        help='node number (default: 99 for all)')


parser.add_argument('-S',
        required=False,
        type=str,
        default='Y',
        help='screen essions (Y to create new (default), E to use existing')


args = parser.parse_args()


hosts = [
        '192.168.5.41', #1
        '192.168.5.42', #2
        '192.168.5.19', #3
        '192.168.5.8', #4
        '192.168.5.9' #5
]

master = '192.168.5.1'

user   = 'pi'

password = 'raspi2020'

m_password = 'raspi2020'

script = '~/code/python/cluster_config.py -v Y -o Y'

screen_cmd = 'screen -S node{a} -p 0 -X stuff \'{b} -c "{c}" -n {a}\'^M'


if args.S in ['Y','y']:
	subprocess.call('pkill screen', shell=True)


if args.n !=99:

	for node in args.n:
		
		if args.S in ['Y','y']:
			subprocess.call('screen -dmS ' + 'node' + str(node), shell=True)


		if args.v in ['Y','y']:
                	print('\n >>> ATTEMPTING NODE: '+str(node)+'...')

		try:
			exec_cmd = screen_cmd.format(a=node, b=script, c=args.c)
			subprocess.call(exec_cmd, shell=True)

		except:
			print("Problem with node "+str(node)+'\n')

	sys.exit()



for node,host in enumerate(hosts):

	if args.S in ['Y','y']:
		subprocess.call('screen -dmS ' + 'node' + str(node+1), shell=True)

	if args.v in ['Y','y']:
                print('\n >>> ATTEMPTING NODE: '+str(node+1)+'...')

	try:

		exec_cmd = screen_cmd.format(a=node+1, b=script, c=args.c)
		subprocess.call(exec_cmd, shell=True)

	except:
		print("Problem with node "+str(node+1)+'\n')
