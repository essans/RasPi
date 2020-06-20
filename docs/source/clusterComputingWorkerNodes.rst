======================
Set-up of Worker Nodes
======================

Connect components:
        - Run power from power-hub to each worker node
        - Connect each worker-node to network switch
        - Connect master-node to internet switch
        
Switch on power to:        
        - Network switch 
        - Master-node
        - Worker-node power-hub
    
------    

Discover IP addresses for each worker node
------------------------------------------

In setting-up the master-node it was assigned a static ip address ``192.168.5.1`` with subnet mask of ``255.255.255.0``.  This can be confirmed with ``ifconfig``

**(1) Scan network**

On the master-node we are going to scan that range using CIDR notation. For example ``192.168.5.0/24`` scans the 256 IP addresses from ``192.168.5.0 to 192.168.5.255``. And, ``192.168.5.0/16`` would scan all 65,534 IP addresses from ``192.168.0.0 to 192.168.255.255``. The first scan would take a few seconds while the latter would take 30-60minutes...

    .. code-block:: bash

        sudo nmap -sn 192.168.5.0/24
  
This will return a list of IP addresses active on our isolated network.  

**(2) Identify each worker node in stack**

Not absolutely necessary (indeed it would be impractical at scale and for remote servers), but we can from the master-node ssh into each pi and execute the following to "flash" the green LED to identify locations:

.. code-block:: bash
    
    sudo sh -c "echo 1 >/sys/class/leds/led0/brightness"
    
By convention we’ll assign node number from the top beginning with 1. Note them down the configuration looks like this:

.. code-block:: bash

    192.168.5.1 Master aka raspi-4b (also reachable via 192.168.1.186 on wlan0)

    192.168.5.41
    192.168.5.42
    192.168.5.19
    192.168.5.8
    192.168.5.9
    
-----


Configure each worker node
--------------------------

In order to update/upgrade the OS on each worker node and make initial configuration changes, I could take a number of approaches:

-- ssh into each node and make these changes one at time. Just about manageable task for 5 nodes, but what if I had 50 nodes?

-- Make all changes on one of the nodes and then clone the card for each of the other 4 nodes. Again a manageable task for 1+4 nodes, but what if I had 1+49 ? What if the worker nodes are not in the same physical location?

-- The approach I take is via the ``fabric`` python package which allows programatic scheduling and running of shell commands over ssh. I can write some code that stores the IP addresses, user names, passwords etc for each node; loop across each of these node while passing the desired command lines we want to run.  More information on the ``fabric`` python package can be found here: https://www.fabfile.org and here: https://docs.fabfile.org/en/2.5/

----

How to manage nodes programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On the master-node create the ``~/code/python`` folder, and then create a ``cluster_config.py`` file and copy/paste code from here: https://github.com/essans/RasPi/blob/master/Clusters/configure_cluster.py

Update the IP addresses, passwords etc and run a ``chmod u+x`` to enable quick running from command line and and then run:

    .. code-block:: bash

        ./cluster_config.py --help

        # returns
        # 
        # execute command across cluster

        # optional arguments:
        # -h, --help  show this help message and exit
        # -v V        Verbose (default: Y)
        # -c C        command to execute (default: 'hostname -I')
        # -m M        include master node (default: N)
        # -n N        node number (default: 99 for all)


Test first using the following which should flash the green LED across each node:

    .. code-block::  bash

        ./cluster_config.py -c 'sudo sh -c "echo 1 >/sys/class/leds/led0/brightness"' -m Y
    
-----

Update/Upgrade OS
^^^^^^^^^^^^^^^^^

**Run an update/upgrade across all worker nodes, and reboot**

    .. code-block::  bash

        ./cluster_config.py -c 'sudo apt-get -y update'

        ./cluster_config.py -c 'sudo apt-get -y upgrade'

        ./cluster_config.py -c 'sudo shutdown -r now’

-----

update localizations
^^^^^^^^^^^^^^^^^^^^

**Check, then update**

    .. code-block:: bash

        ./cluster_config.py -c ‘timedatectl'
    
Raspberry Pi boards usually ship with the UK localization so we’ll need to update if we’re (say) based in New York and the master is configured as such. The following will list available timezones: ``timedatectl list-timezones``.  And then to update:

    .. code-block:: bash

        ./cluster_config -c 'sudo timedatectl set-timezone America/New_York'

        ./cluster_config.py -c ‘timedatectl'  # to confirm updates

-----

      
Update locale settings
^^^^^^^^^^^^^^^^^^^^^^
  
**Check, then update.** 

    .. code-block:: bash

        ./cluster_config.py -c ‘locale'
        
If updates are needed then first check that the locale is available:

.. code-block:: bash
    
    ./cluster_config.py -c ‘locale -a'
    

If not then generate as needed. In this case for en_US first uncomment it in the locale.gen file if necessary.

.. code-block:: bash

    ./cluster_config.py -c 'sudo sed -i "/en_US.UTF-8/s/^#[[:space:]]//g" /etc/locale.gen' -n 1

    # removes ‘# ‘
    # to recomment a line with a trailing space:
    # sed -i '/<pattern>/s/^/# /g' file


    ./cluster_config.py -c 'sudo locale-gen'
    
    ./cluster_config.py -c 'sudo update-locale LANG=en_US.UTF-8'
    
    ./cluster_config.py -c 'locale'  # to confirm
 
-----
    
Change passwords
^^^^^^^^^^^^^^^^

.. code-block:: bash

    .cluster_config.py -c 'echo -e "raspberry\nNewPassword\nNewPassword" | passwd'
    
    # where NewPassword is the desired new password
    
Now update the passwords in the ``cluster_config.py`` script

-----

Change hostnames
^^^^^^^^^^^^^^^^

Update ``hostname`` for each pi from the ``raspberrypi`` default to ``node1``, ``node2`` etc.  I could do these one at a time on each node via ``raspi-config`` or by updating these files:

.. code-block:: bash

        /etc/hosts
        /etc/hostname


..but instead I'll attempt this is one shot across all worker nodes remotely.

First I'll confirm the hostname of each node:

.. code-block:: bash

        .cluster_config.py -c 'hostname -s'
        
These should all come back as ``raspberrypi``.  In the above mentioned files I need to replace ``raspberrypi`` with ``node1``, ``node2`` etc.  This could be done one at a time by passing the following to ``./cluster_config.py``:

.. code-block:: bash

        sed -i 's/raspberrypi/node1/g' /etc/hosts   #s to replace, /g global
        sed -i 's/raspberrypi/node2/g' /etc/hosts
        sed -i 's/raspberrypi/node3/g' /etc/hosts
        sed -i 's/raspberrypi/node4/g' /etc/hosts
        sed -i 's/raspberrypi/node5/g' /etc/hosts

        # and then repeat for /etc/hostname

It's more interesting though to consider a "wrapper" script that calls ``./cluster_config.py`` in a loop:

.. code-block:: python

        #!/usr/bin/env python3

        import sys
        import subprocess


        cmds_to_execute =   {1:"'sudo sed -i \"s/raspberrypi/node1/g\" /etc/hosts'",   
                             2:"'sudo sed -i \"s/raspberrypi/node2/g\" /etc/hosts'",
                             3:"'sudo sed -i \"s/raspberrypi/node3/g\" /etc/hosts'",
                             4:"'sudo sed -i \"s/raspberrypi/node4/g\" /etc/hosts'",
                             5:"'sudo sed -i \"s/raspberrypi/node5/g\" /etc/hosts'"
                            }

        for node,command in cmds_to_execute.items():

                cmd_to_send = "./cluster_config.py -c " + command + " -n " +str(node)

                subprocess.call(cmd_to_send, shell = True)  
                
Above script is saved as ``cluster_commands.py`` and then run from the command line.  Then re-rerun after updating with ``/etc/hostname``.

Once successfully run reboot the worker nodes with ``./cluster_config.py -c 'sudo shutdown -r now’`` and then confirm that the hostnames as done earlier.




