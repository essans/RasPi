#!/usr/bin/env python3

#Execute commands from master node across 1 or all worker nodes, with option to also run on master.

# run chmod u+x clustercmd.py from command line

# ./clustercmd --help  <--- see all options

# ./clustercmd -c 'hostname -I', -m    <- execute 'hostname -I' across all nodes incl. Master

# ./clustercmd -c 'hostname -I', -n 0 1 5 <- execute across nodes 0 (master), 1 and 5 only

# ./clustercmd -c 'hostname -I', -p <- lowercase -p to use passwords instead of sshkeys 

# ./clustercmd -c 'hostname -I', -P <- capital -P to execute in parallel

# add following line to ~/.bashrc file to enable global execution without './'
# alias clustercmd="python3 ~/code/python/cluster"   <replace with actual location of .py file>

# need to add logging

###################################



import sys
import argparse
import subprocess

from myconfigs import cluster1 as cluster

from fabric import Connection


def get_args():

	parser = argparse.ArgumentParser(description="Execute command across cluster")

	parser.add_argument('-p','--pswd',
 		action='store_true',
                help="use passwords from config file instead of ssh keys")


	parser.add_argument('-P','--Parallel',
                action='store_true',
                help="execute in parallel (default is serial execution")


	parser.add_argument('-l','--logging',
	        required=False,
	        action='store_true',
	        help="log only instead of printing commands to screen")


	parser.add_argument('-q','--quiet',
	        required=False,
	        action='store_true',
	        help="execute quietly and do not show output (default: show output)")


	parser.add_argument('-c','--cmd',
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



def cmd_macros(args):
	
	cmd_dict = {
		'ledoff':'echo 0 | sudo tee /sys/class/leds/led1/brightness',
		'ledon':'echo 1 | sudo tee /sys/class/leds/led1/brightness',
		}

	if args.cmd in cmd_dict.keys():
		return cmd_dict[args.cmd]

	else:
		return args.cmd



def send_cmd(args, node, node_ip):

	if args.pswd:
                credentials =  {'password': cluster.passwords[node]}

	else:
		credentials = {'password': cluster.passwords[node],
			       'key_filename':cluster.sshkeys[node]}

	try:
		c = Connection(
			node_ip,
			user = cluster.users[node],
			connect_kwargs = credentials)

		result = c.run(args.cmd, hide = args.quiet)

	except:
		print('Problem with node {}\n'.format(node))



def serial_execution(args):

	for node,node_ip in cluster.nodes.items():

		if (node==0 and not args.master and args.nodes==99) \
			or (args.nodes!=99 and node not in args.nodes):

			continue

		if not args.logging:
                	print('\n >>> ATTEMPTING NODE: {}...'.format(node))

		send_cmd(args, node, node_ip)



def parallel_execution(args):

	script = '~/code/python/cluster/clustercmd.py '

	screen_cmd = 'screen -S node{a} -p 0 -X stuff \'{b} -c "{c}" -n {a}\'^M'

	args_to_send = '{a}{b}{c}{d}'.format(
				a = args.cmd,
				b = ' -p' if args.pswd else '',
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
			print(exec_cmd)

		except:
			print("Problem with node "+str(node)+'\n')



def main():
	args = get_args()

	args.cmd = cmd_macros(args)

	if args.Parallel:
		parallel_execution(args)
	
	else:
		serial_execution(args)

	

if __name__ == '__main__':
	main()
