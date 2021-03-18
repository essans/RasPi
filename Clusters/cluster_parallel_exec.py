#!/usr/bin/env python3

#!/usr/bin/env python3

import subprocess
import argparse
from myconfigs import cluster1 as cluster
from fabric import Connection

def get_args():

	parser = argparse.ArgumentParser(description="execute command across cluster")


	parser.add_argument('-p','--password',
 		action='store_true',
                help="use passwords from config file instead of ssh keys")


	parser.add_argument('-l','--logging',
	        required=False,
	        action='store_true',
	        help="log only instead of printing commands to screen")


	parser.add_argument('-q','--quiet',
	        required=False,
	        action='store_true',
	        help="execute quietly without showing output (default: show output)")


	parser.add_argument('-c','--command',
		required=False,
		type=str,
		default='echo $(hostname), $(hostname -I)',
		help="command to execute (default: 'hostname -I')")

	parser.add_argument('-m','--master',
		required=False,
		action='store_true',
		help='include execution on master node')

	parser.add_argument('-n','--nodes',
	        required=False,
		nargs='*',
	        type=int,
	        default=99,
	        help='node numbers (default: 99 for all)')

	args = parser.parse_args()


	return args


def main():

	args = get_args()

	script = '~/code/python/cluster/cluster_serial_exec.py '

	screen_cmd = 'screen -S node{a} -p 0 -X stuff \'{b} -c "{c}" -n {a}\'^M'

	args_to_send = '{a}{b}{c}{d}'.format(
				a = args.command,
				b = ' -p' if args.password else '',
				c = ' -l' if args.logging else '',
				d = ' -q' if args.quiet else '')


	subprocess.call('pkill screen', shell=True)


	for node,node_ip in cluster.nodes.items():

		if (node==0 and not args.master and args.nodes==99) \
			or (args.nodes!=99 and node not in args.nodes):

			continue

		
		subprocess.call('screen -dmS ' + 'node' + str(node), shell=True)

		if not args.logging:
                	print('\n >>> ATTEMPTING NODE: {}...'.format(node))
	

		try:
			exec_cmd = screen_cmd.format(a = node, b = script, c = args_to_send)
			subprocess.call(exec_cmd, shell=True)

		except:
			print("Problem with node "+str(node)+'\n')


if __name__ == '__main__':
	
	main()
