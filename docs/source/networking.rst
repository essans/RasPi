==========
Networking
==========


Create wireless access point
----------------------------

Background
^^^^^^^^^^
For the past few months I've had a Raspberry Pi 4 (raspi-4a) connected to my home network via ethernet cable and running 24/7. I can remote into the device using ssh from both within my local network and also from outside using port forwarding. 

There are also other Raspberry Pi boards that connect to the same router via wifi.  There are also computers, phones, iPads and other wireless devices that connect to the same wifi router.  While every device has its own MAC address and operates on an assigned channel there is still a chance of conflicts, latency, and other non-optimal behavior when not using a router not designed to handle that capacity.

.. image:: images/raspi4a_accesspoint.png
    :align: center
    :alt: raspi4a_as_accesspoint

-----

Objective
^^^^^^^^^

Reduce number of wifi devices connecting to the internet router by directing raspberry pi wireless traffic via the raspi-4a which is connected to the internet via ethernet. This raspi-4a device which acting as a wireless access point will broadcast its own SSID ("RAPI-NET").  The Raspi4a will still function normally as a raspberry pi while simultaneouly offering wireless access to any device with correct credentials. 

.. image:: images/raspi4a_network.png
    :align: center
    :alt: network


-----

Access Point set-up
^^^^^^^^^^^^^^^^^^^

This involves changes various network configurations so it's a good idea to clone the SD Card so that there is a point to revert any changes back to.  Also, changes in network settings may result in lost SSH connection so use a monitor and keyboard to be on the safe side...

**(1) Check for updates**

.. code-block:: bash

    sudo apt-get update
    sudo apt-get upgrade
    
**(2) Install required packages**

.. code-block:: bash

    sudo apt-get install hostapd   # to create a wireless hotspot
    sudo apt-get install dnsmasq   # easy-to-use DHCP and DNS server
    sudo apt install bridge-utils  # to enable bridge between eth0 and wireless 
    
**(3) Switch off servces before changing any configurations:**

.. code-block:: bash

    sudo systemctl stop hostapd
    sudo systemctl stop dnsmasq
    
**(4) Edit the dhcpcd configuration file ``/etc/dhcpcd.conf`` and add:**

.. code-block:: bash

    # These first 2 lines were added later after lots of trial and error... 
    # Both are needed to ensure that the bridge works correctly.
    # They stop the eth0 and wlan0 ports being allocated IP 
    # addresses by the DHCP client on the Raspberry Pi

    denyinterfaces wlan0    
    denyinterfaces eth0     


    # Next configure a static IP for the wlan0 interface

    interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant


    # static IP address to enable ssh and also accessing 
    # the internet from the raspberry pi.
    # This bit was also discovered after some trial and error...

    interface br0
    static ip_address=192.168.1.184/24  # assigning to AP
    static routers=192.168.1.1
    static domain_name_servers=8.8.8.8
    

**(5) Restart the dhcp service:**

.. code-block:: bash
    
    sudo service dhcpcd restart
    
**(6) Configure the DHCP server/masq configuration file ``/etc/dnsmasq.conf`` by adding:**

.. code-block:: bash

    interface=wlan0
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h    # addresses for clients
    
The way to undersand this is that for ``wlano`` we are going to provide IP addresses between ``192.168.4.2 and 192.168.4.20``, with a lease time of 24 hours. If providing DHCP services for other network devices (e.g. eth0), we would add more sections with the appropriate interface header, with the range of addresses intended to provide to the additional interface.

There are many more options for dnsmasq. See `dnsmasq documentation <http://www.thekelleys.org.uk/dnsmasq/doc.html>`_  for more details.

**(7) Restart service**

.. code-block:: bash

    sudo systemctl start dnsmasq
    

    
