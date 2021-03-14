#!/usr/bin/env python3

import subprocess
import argparse

from myconfigs import cluster1 as cluster


def get_args():

	parser = argparse.ArgumentParser(description="copy files to nodes")

	parser.add_argument('-verbose',
		required=False,
		type=str,
		default='Y',
		help="Verbose (default: Y)")

	parser.add_argument('-filename',
		required=True,
		type=str,
		help="file to copy")

	parser.add_argument('-dest',
        	required=False,
        	type=str,
        	help="destination (eg: ~/code/filename.ext  - default is home folder with same filename")

	parser.add_argument('-nodes',
        	required=True,
		nargs='*',
        	type=int,
        	help='destination node number(s)')


	args = parser.parse_args()

	if args.dest is None:
		args.dest = args.filename.split('/')[-1]


	return args



def main():
	args = get_args()

	for node in args.nodes:


		if args.verbose in ['Y','y']:
                	print('\nATTEMPTING NODE: {}...'.format(node))

		try:

			xfer_cmd = 'sshpass -p {p} scp {f} {u}@{n}:{d}'.format(
									p = cluster.passwords[node],
									f = args.filename,
									u = cluster.users[node],
									n = cluster.nodes[node],
									d = args.dest)	

			if args.verbose in ['Y','y']:
                        	print(' >> executing: ' + xfer_cmd.replace(cluster.passwords[node],'<pwd>'))

			subprocess.call(xfer_cmd, shell=True)			


		except:
			print("Problem with node "+str(node)+'\n')



if __name__ == '__main__':
	main()
