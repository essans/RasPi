Overview
========

This section will document the set-up, and list the components needed for an initial configuration of a master node + worker nodes operating on an isolated part of the network.


Architecture / Framework
************************
The cluster will comprise of 5 Raspberry Pi 3 Model B+ (1gb RAM) worker nodes, powered by a USB power supply unit, and networked together via a simple unmanaged switch.  The master node will be a Raspberry Pi 4 (4gb RAM) on a separate power-supply wired into the same network switch

The master-node will connect to the internet via wireless LAN.  The worker nodes will only have access to the internet when allowed/needed via the master-node using "IP Masquerading" gateway.

Operating system on master and worder nodes will be Raspbian/Debian flavor of Linux.


Hardware Schematic
******************


-diagram here-


Parts List
**********

-table here-






