#!/usr/bin/env python3

#Execute commands from master node across 1 or all worker nodes, with option to also run on master.

# ./cluster_serial_exec --help  <--- see all options

# ./cluster_serial_exec -c 'hostname -I', -m    <- execute 'hostname -I' across all nodes incl. Master

# ./cluster_serial_exec -c 'hostname -I', -n 0 1 5 <- execute across nodes 0 (master), 1 and 5 only

# ./cluster_serial_exec -c 'hostname -I', -p <- use passwords instead of sshkeys 

# need to add logging

###################################


#!/usr/bin/env python3

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



def exec_across_nodes(args):

	for node,node_ip in cluster.nodes.items():

		if (node==0 and not args.master and args.nodes==99) \
			or (args.nodes!=99 and node not in args.nodes):

			continue


		if not args.logging:
                	print('\n >>> ATTEMPTING NODE: {}...'.format(node))



		if args.password:
			credentials = {'password': cluster.passwords[node]}

		else:
			credentials = {'password': cluster.passwords[node],
                                       'key_filename':cluster.sshkeys[node]}


		try:
			c = Connection(
				node_ip,
				user = cluster.users[node],
				connect_kwargs = credentials)

			result = c.run(args.command, hide = args.quiet)

		except:
			print('Problem with node {}\n'.format(node))


def main():
	args = get_args()
	exec_across_nodes(args)


if __name__ == '__main__':
	main()
