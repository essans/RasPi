### Set-up of Master Node

#### First, install and configure operating system

(1) See https://raspi-recipes.readthedocs.io/en/latest/initialSetup.html#

(2) Install python in case not already installed, along with the [fabric package](http://www.fabfile.org) that I will need later.

```sh
sudo apt install python3-pip

sudo pip3 install fabric
```

----
<br>

#### Configure Master Node as conduit for cluster internet access.

I want the Master Node to be the only device on the cluster that actually connects to the internet. When worker nodes require internet access then the will connect via the Master Node if allowed.  The set-up here is based on what was learned when configuring another Raspberry Pi to provide service as a secondary [access point](https://github.com/essans/RasPi/blob/master/networking/accessPoint.md).

(1) Install the linux command line utility [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) and then stop the service before make the configuration changes

```sh
sudo apt-get install dnsmasq

sudo systemctl stop dnsmasq
```

<br>

(2) Edit the DHCP client daemon configuration file
```sh
sudo nano /etc/dhcpcd.conf
```

...adding the following at the bottom in order to assign a static IP address to the master node:

```sh
interface eth0
static ip_address=192.168.5.1/24 
```

Save and exit, and then

```sudo service dhcpcd restart```

<br>

(3) I want to control the assignment of IP address to the the worker nodes that will live on the sub-network and access this raspberry pi for internet access.  To do that I need to configure the ```dnsmasq.conf``` file:

```sh
sudo nano /etc/dnsmasq.conf
```

After making sure that EVERY line is commented out (most usually but there might be two at the bottom) add the following lines:

```sh
interface=eth0 #internet service to the nodes via ethernet 
dhcp-range=192.168.5.2,192.168.5.64,255.255.255.0,24h #range of IP addresses
```

```sh
sudo systemctl start dnsmasq  #start the service
```

(4) Enable IP forwarding in this file: 

```sudo nano /etc/sysctl.conf``` 

by uncommenting this line:

```sh
net.ipv4.ip_forward=1
```

(5) Now I need to update ```iptables``` to configure the ip packet filter rules in allow all worker nodes to essentially use the IP address of the master node when connecting to the internet.  This is known as masquerading and the firewall keeps track of the incoming and outgoing connections (ie how to directly traffic to/from the right node) using Network Address Translation.  Essentially by keeping tracking of ports and MAC addresses. 

```sh
sudo iptables -t nat -A  POSTROUTING -o wlan0 -j MASQUERADE
```

and then save the rules so they are not lost upon reboot:

```sh
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

Then edit this file so that rules are installed upon boot:

```sh
sudo nano /etc/rc.local
```

and add the following line just above the "exit 0":

```sh
iptables-restore < /etc/iptables.ipv4.nat
```

now reboot the pi:

```sh
sudo shutdown -r
```

To list rules in iptables:

```
sudo iptables -t nat -L
```



---
<br>

The following diagram illustrates how this masquerading and network address translation will work once the worker nodes are set-up:

![](https://github.com/essans/RasPi/blob/master/images/raspi_cluster_nat.png)

The way it works is as follows:

(1) When the worker nodes 1-5 come on line they will request an IP address the [DHCP](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#Discovery) server running on the master node.  Either a new one, or the previously assigned one if available.  At this point the IP address for each note is mapped to its corresponding MAC address.

(2) If node 2 seeks to connect to the internet (eg via a ping request sent via TCP on port 22) then that will travel to the master node.  The master node using the DNS Masquerading will mask node2's IP address with it's own which will then travel to the router before itself betting masked with the router's public IP address.

At each step of the way mappings and tables are maintained so that when a response is received from the internet it knows how to find its way back to node2 which sits in an isolated part of the network.

![](https://github.com/essans/RasPi/blob/master/images/raspi_cluster_node2_ping.png)

Node 2 can communicate outside of the cluster but nothing outside the isolated network can communicate in.

To see this in action I can use ```tcpdump```

```sh
sudo apt-get install tcpdump
```

```sh
sudo tcpdump -i eth0 -en
```
---
<br>

The master node is now ready.  It might make sense to [back-up](https://medium.com/@ccarnino/backup-raspberry-pi-sd-card-on-macos-the-2019-simple-way-to-clone-1517af972ca5).

[Next](): Configure each node.


















