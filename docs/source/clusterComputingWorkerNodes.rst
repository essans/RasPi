Set-up of Worker Nodes
----------------------

Connect and power-up everything.


Discover IP addresses for each worker node
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to update/upgrade the OS on each worker node and make initial configuration changes, I could take a number of approaches:

(a) ssh into each node and make these changes one at time. Just about manageable task for 5 nodes, but what if I had 50 nodes?

(b) Make all changes on one of the nodes and then clone the card for each of the other 4 nodes. Again a manageable task for 1+4 nodes, but what if I had 1+49 ? What if the worker nodes are not in the same physical location?

(c) The approach I take is via the fabric python package which allows programatic scheduling and running of shell commands over ssh. I can write some code that stores the IP addresses, user names, passwords etc for each node; loop across each of these node while passing the desired command lines we want to run.

----

**(1) Create script for managing nodes programmatically**

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
    

**Run an update/upgrade across all worker nodes, and reboot**

    .. code-block::  bash

        ./cluster_config.py -c 'sudo apt-get -y update'

        ./cluster_config.py -c 'sudo apt-get -y upgrade'

        ./cluster_config.py -c 'sudo shutdown -r now’


**(3) Check/update localizations**

    .. code-block:: bash

        ./cluster_config.py -c ‘timedatectl'
    
Raspberry Pi boards usually ship with the UK localization so we’ll need to update if we’re (say) based in New York and the master is configured as such. The following will list available timezones: ``timedatectl list-timezones``.  And then to update:

    .. code-block:: bash

        ./cluster_config -c 'sudo timedatectl set-timezone America/New_York'

        ./cluster_config.py -c ‘timedatectl'  # to confirm updates
        
**(4) Check/update locale settings.** 

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
    
    
**(5) Change passwords:**

.. code-block:: bash

    .cluster_config.py -c 'echo -e "raspberry\nNewPassword\nNewPassword" | passwd'
    
    # where NewPassword is the desired new password
    
Now update the passwords in the ``cluster_config.py`` script


**(6) Change hostnames**

Update ``hostname`` for each pi from the ``raspberrypi`` default to ``node-1``, ``node-2`` etc.  As each hostname will be different I need call the ``cluster_config.py`` script from a loop.