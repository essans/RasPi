==========
Networking
==========


Create wireless access point
----------------------------

Background
^^^^^^^^^^
For the past few months I've had a Raspberry Pi 4 (raspi-4a) connected to my home network via ethernet cable and running 24/7. I can remote into the device using ssh from both within my local network and also from outside using port forwarding. 

There are also other Raspberry Pi boards that connect to the same router via wifi.  There are also computers, phones, iPads and other wireless devices that connect to the same wifi router.  While every device has its own MAC address and operates on an assigned channel there is still a chance of conflicts, latency, and other non-optimal behavior when not using a router not designed to handle that capacity.


Objective
^^^^^^^^^

Reduce number of wifi devices connecting to the internet router by directing raspberry pi wireless traffic via the raspi-4a which is connected to the internet via ethernet. This raspi-4a device which acting as a wireless access point will broadcast its own SSID ("RAPI-NET").  The Raspi4a will still function normally as a raspberry pi while simultaneouly offering wireless access to any device with correct credentials. 

Access Point set-up
^^^^^^^^^^^^^^^^^^^
