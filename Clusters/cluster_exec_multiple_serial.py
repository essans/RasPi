#!/usr/bin/env python3

import sys
import subprocess


cmds_to_execute =   {1:"'sudo sed -i \"s/raspberrypi/node1/g\" /etc/hostname'",   
                     2:"'sudo sed -i \"s/raspberrypi/node2/g\" /etc/hostname'",
                     3:"'sudo sed -i \"s/raspberrypi/node3/g\" /etc/hostname'",
                     4:"'sudo sed -i \"s/raspberrypi/node4/g\" /etc/hostname'",
                     5:"'sudo sed -i \"s/raspberrypi/node5/g\" /etc/hostname'"

                    }

for node,command in cmds_to_execute.items():

        cmd_to_send = "./cluster_exec_serial.py -c " + command + " -n " +str(node)

        subprocess.call(cmd_to_send, shell = True)
