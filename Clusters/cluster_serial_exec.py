#!/usr/bin/env python3

#Execute commands from master node across 1 or all worker nodes, with option to also run on master.

# ./cluster_exec_serial --help  <--- see all options

# ./cluster_exec_serial -c 'hostname -I', -m Y    <- execute 'hostname -I' across all nodes incl. Master

# ./cluster_exec_serial -c 'hostname -I', -n 0 1 5 <- execute across nodes 0 (master), 1 and 5 only


###################################


#!/usr/bin/env python3

import sys
import argparse

from myconfigs import cluster1 as cluster

from fabric import Connection


def get_args():

	parser = argparse.ArgumentParser(description="execute command across cluster")

	parser.add_argument('-verbose',
	        required=False,
	        type=str,
	        default='Y',
	        help="verbose (default: Y)")


	parser.add_argument('-output',
	        required=False,
	        type=str,
	        default='Y',
	        help="hide output (default: Y)")


	parser.add_argument('-cmd',
		required=False,
		type=str,
		default='echo $(hostname), $(hostname -I)',
		help="command to execute (default: 'hostname -I')")

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
	        help='node numbers (default: 99 for all)')


	args = parser.parse_args()


	if args.output in ['Y','y']:
		args.output = False

	else:
		args.output = True


	return args



def exec_across_nodes(args):

	for node,node_ip in cluster.nodes.items():

		if (node==0 and not args.master in ['Y','y'] and args.nodes==99) \
			or (args.nodes!=99 and node not in args.nodes):
			
			continue


		if args.verbose in ['Y','y']:
                	print('\n >>> ATTEMPTING NODE: {}...'.format(node))


		try:
			c = Connection(
				node_ip,
				user = cluster.users[node],
				connect_kwargs={
					'password': cluster.passwords[node],
					'key_filename':cluster.sshkeys[node]})

			result = c.run(args.cmd, hide = args.output)

		except:
			print('Problem with node {}\n'.format(node))


def main():
	args = get_args()
	exec_across_nodes(args)


if __name__ == '__main__':
	main()
