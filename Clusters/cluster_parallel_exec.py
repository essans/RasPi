#!/usr/bin/env python3


import sys
import subprocess
import argparse

from myconfigs import cluster1 as cluster

from fabric import Connection


def get_args():
	parser = argparse.ArgumentParser(description="execute command in parallel across worker nodes")

	parser.add_argument('-verbose',
        	required=False,
        	type=str,
        	default='Y',
        	help="Verbose (default: Y)")

	parser.add_argument('-output',
	        required=False,
	        type=str,
	        default='Y',
	        help="show output (default: Y)")

	parser.add_argument('-cmd',
		required=False,
		type=str,
		default='hostname',
		help="command to execute (default: 'hostname')")

	parser.add_argument('-master',
		required=False,
		type=str,
		default='N',
		help='include master node (default:  N)')

	parser.add_argument('-nodes',
	        required=False,
	        nargs='*',
	        type=int,
	        default=99,
	        help='node number (default: 99 for all)')

	parser.add_argument('-screens',
	        required=False,
	        type=str,
	        default='Y',
	        help='screen essions (Y to create new (default), E to use existing')


	args = parser.parse_args()

	if args.output in ['Y','y']:
		args.output = False

	else:
		args.output = True


	return args




def main():

	args = get_args()

	script = '~/code/python/cluster_exec_serial.py -v Y -o Y'
	
	screen_cmd = 'screen -S node{a} -p 0 -X stuff \'{b} -c "{c}" -n {a}\'^M'


	if args.screens in ['Y','y']:
		subprocess.call('pkill screen', shell=True)


	for node,node_ip in cluster.nodes.items():
			
		if (node==0 and not args.master in ['Y','y'] and args.nodes==99) \
			or (args.nodes!=99 and node not in args.nodes):
			
			continue


		if args.screens in ['Y','y']:
			subprocess.call('screen -dmS ' + 'node' + str(node), shell=True)

		if args.verbose in ['Y','y']:
                	print('\n >>> ATTEMPTING NODE: {}...'.format(node))
	
		try:

			exec_cmd = screen_cmd.format(a=node, b=script, c=args.cmd)
			subprocess.call(exec_cmd, shell=True)

		except:
			print("Problem with node "+str(node)+'\n')



if __name__ == '__main__':
	
	main()
