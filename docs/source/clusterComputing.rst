=================
Cluster Computing
=================

Overview
--------


This recipe documets the steps taken in setting-up a cluster of Raspberry Pis.  The idea is to try a few different approaches and in doing so reinforce understanding of some of the principles relating to linux networking, distributed computing and a few other things...

-----

Architecture/Framework
----------------------
The architecture for this first cluster will comprise of 5 Raspberry Pi 3 Model B+ worker nodes, powered by a USB power supply unit and networked together via a simple unmanaged switch. The master node will be a Raspberry Pi 4 (4gb RAM) on a separate power-supply wired into the same network switch.

The master node will connect to the internet via wireless LAN and using "IP Masquerading" will provide gateway access to the internet for the worker nodes only when needed.

Operating system on master and worker nodes will be Raspbian/Debian flavour of linux.

-----

**Schematic**

.. image:: images/raspi_cluster_diagram_v1.png
    :align: center
    :alt: cluster

-----

**Parts List**


+----------+-------------------------------------------------------------+-----------+---------+
| Quantity |              Part                                           | Source    |   Cost  |
+==========+=============================================================+===========+=========+
|    1     | Raspberry Pi 4 (4gb)                                        | Canakit   |  $  55  |
+----------+-------------------------------------------------------------+-----------+---------+
|    5     | Raspberry Pi 3 Model B+                                     | Canaki    |  $ 175  |
+----------+-------------------------------------------------------------+-----------+---------+
|    5     | Cat5e 1ft Ethernet patch cable                              | Amazon    |  $   8  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | Cat6 18in Ethernet patch cable                              | Amazon    |  $   5  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | GeauxRobot 6 layer dog bone stack                           | Amazon    |  $  32  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | Clear Case for Raspberry Pi 4                               | Amazon    |  $   5  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | Anker 60W PowerPort 6-port wall charger (2.4A per port max) | Amazon    |  $  30  |
+----------+-------------------------------------------------------------+-----------+---------+
|    6     | Sabrent 22AWG 1ft micro USB to USB cables                   | Amazon    |  $   8  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | 15W (5v, 3A) power supply (Raspi 4)                         | Pi Shop   |  $   8  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | NETGEAR 8-Port Gigabit Ethernet Unmanaged Switch            | Amazon    |  $  22  |
+----------+-------------------------------------------------------------+-----------+---------+
|    1     | Powerstrip with independent switches                        | Amazon    |  $  20  |
+----------+-------------------------------------------------------------+-----------+---------+
|    6     | SanDisk 32GB MicroSD HC ultra 80mb/s (non A1)               | Amazon    |  $  36  |
+----------+-------------------------------------------------------------+-----------+---------+
|          |                                                             |           |  $ 404  |
+----------+-------------------------------------------------------------+-----------+---------+

-----


Set-up of Master Node
---------------------
This is the Raspberry pi which will control and manage the set of worker nodes.  


Install and configure operating system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(1) See: https://raspi-recipes.readthedocs.io/en/latest/initialSetup.html#

(2) Install python (in case not already installed), along with the `fabric package <http://www.fabfile.org/>`_ that will be needed later.

    .. code-block:: bash

        sudo apt install python3-pip

        sudo pip3 install fabric
        
(3) Install other tools that we'l need

    .. code-block:: bash
        sudo apt install tcpdump


------

Configure Master Node as conduit for internet access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Master Node will be the sole device on the cluster that connects to the internet. When worker nodes require internet access then they will connect via the Master Node (if allowed). The set-up here is based on what was learned when configuring another Raspberry Pi to provide service as a secondary `access point <https://raspi-recipes.readthedocs.io/en/latest/networking.html#create-wireless-access-point>`_ .

**(1) Install linux command line utility dnsmasq and then stop the service before making configuration changes**

    .. code-block:: bash

        sudo apt-get install dnsmasq

        sudo systemctl stop dnsmasq
        
*ref: https://en.wikipedia.org/wiki/Dnsmasq*

**(2) Edit the DHCP client daemon configuration file**

    .. code-block:: bash

            sudo nano /etc/dhcpcd.conf
            
...adding the following lines at the bottom in order to assign a static IP address to the master node:

    .. code-block:: bash

        interface eth0
        static ip_address=192.168.5.1/24 
        
Save, exit, and then restart the service:

    .. code-block:: bash

        sudo service dhcpcd restart
        

**(3) Control assignment of IP addresses to the worker nodes:**

    .. code-block:: bash

        sudo nano /etc/dnsmasq.conf
        
After making sure that *every* line is commented out (usually the case, but there might be two at the bottom) add the following lines:

    .. code-block:: bash

        interface=eth0 # internet service to the nodes via ethernet 
        dhcp-range=192.168.5.2,192.168.5.64,255.255.255.0,24h # range of IP addresses
    
save, exit and then restart the service:

    .. code-block:: bash

        sudo systemctl start dnsmasq
        
**(4) Enable IP forwarding:**

    .. code-block:: bash

        sudo nano /etc/sysctl.conf
    
uncomment/enable this line:

    .. code-block:: bash
        net.ipv4.ip_forward=1
        
**(5) Now I need to update iptables to configure the ip packet filter rules** 
This is needed in order to allow all worker nodes to essentially use the IP address of the master node when connecting to the internet. This is known as *masquerading* and the firewall keeps track of the incoming and outgoing connections (ie how to directly traffic to/from the relevant node) using Network Address Translation (NAT). Essentially by keeping tracking of ports and MAC addresses.

    .. code-block:: bash

        sudo iptables -t nat -A  POSTROUTING -o wlan0 -j MASQUERADE
        
and then save the rules so they are not lost upon reboot:

    .. code-block:: bash

        sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"


Then edit this file so that rules are installed upon boot:

    .. code-block:: bash

        sudo nano /etc/rc.local
    
and add the following line just above the "exit 0":

    .. code-block:: bash

        iptables-restore < /etc/iptables.ipv4.nat
    
Now reboot the master node.   To list the rules in iptables:


    .. code-block:: bash

        sudo iptables -t nat -L
    
-----

The following diagram illustrates how *masuerading* and network address translation will work once all nodes are set-up:

.. image:: images/raspi_cluster_nat.png
    :align: center
    :alt: clusterInternetAccess


The way it works is as follows:

(1) When the worker nodes 1-5 come on line they will request an IP address the `DHCP <https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#Discovery>`_ server running on the master node.  Either a new one, or the previously assigned one if available.  At this point the IP address for each note is mapped to its corresponding MAC address.

(2) If node 2 seeks to connect to the internet (eg via a ping request sent via TCP on port 22) then that will travel to the master node.  The master node using the DNS Masquerading will mask node2's IP address with it's own which will then travel to the router before itself betting masked with the router's public IP address.

At each step of the way mappings and tables are maintained so that when a response is received from the internet it knows how to find its way back to node2 which sits in an isolated part of the network.

.. image:: images/raspi_cluster_node2_ping.png
    :align: center
    :alt: clusterInternetAccess

Node 2 can communicate outside of the cluster but nothing outside the isolated network can communicate in.

This can be seen in action using ``tcpdump``

    .. code-block:: bash

        sudo tcpdump -i eth0 -en
    

The master node is now ready.  It might make sense to `back-up <https://medium.com/@ccarnino/backup-raspberry-pi-sd-card-on-macos-the-2019-simple-way-to-clone-1517af972ca5>`_.

    
    
    
    
    
    
    
        
        
