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


Objective
^^^^^^^^^

Reduce number of wifi devices connecting to the internet router by directing raspberry pi wireless traffic via the raspi-4a which is connected to the internet via ethernet. This raspi-4a device which acting as a wireless access point will broadcast its own SSID ("RAPI-NET").  The Raspi4a will still function normally as a raspberry pi while simultaneouly offering wireless access to any device with correct credentials. 

.. image:: images/raspi4a_network.png
    :align: center
    :alt: network


Access Point set-up
^^^^^^^^^^^^^^^^^^^

(1) Check for updates

.. code-block:: bash

    sudo apt-get update
    sudo apt-get upgrade
    
(2) Install required packages

.. code-block:: bash

    sudo apt-get install hostapd   #package that lets us create a wireless hotspot
    sudo apt-get install dnsmasq   #easy-to-use DHCP and DNS server
    sudo apt install bridge-utils  #to enable bridge between eth0 and wireless 
