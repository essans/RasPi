### Set-up of Master Node

#### First, install and configure operating system
For this cluster I will use the "Rasbian" operating system which is based on the debian linux distribution and provided by the Raspberry Pi Foundation.

(1) Download and save in a folder the latest Rasbian images from [here](https://www.raspberrypi.org/downloads/raspbian/)
  - For the master node use the [full version](https://downloads.raspberrypi.org/raspbian_full_latest)
  - For the worker nodes use [light version](https://downloads.raspberrypi.org/raspbian_lite_latest) which does not have a GUI, nor any of the other software.
    
(2) Flash the image onto an SD Card using [etcher](https://www.balena.io/etcher/) for Mac OS. 

(3) In the boot partition I create an empty file to enable ssh

```bash
sudo diskutil mount /dev/disk2s1  #or whatever the boot partition is

cd /volumes/boot

touch ssh
```

(4) Enable connection to wifi by creating a ```wpa_supplicant.conf``` file in the same boot partition and input following information:

```bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
    key_mgmt=WPA-PSK
}
```
Save the file and exit.  Unmount and eject the SD card and insert into the Raspberry Pi and power on.

<br>

(5) Login into the router portal via ```http://192.168.1.1``` in order to find out what IP address the router has assigned to the new device that is now connected to the LAN.  I coule also have used a network scanner.  Then ssh into the pi:

```ssh pi@192.168.1.186```

<br>

(6) Update OS and software in the usual way:

```bash
sudo apt-get update

sudo apt-get upgrade    #or full-upgrade
```

<br>

(7) While likely not necessary any more I ensure the file system is expanded:

```sudo raspi-config --expand-rootfs```

<br>

(8) and then update the usual things:

```bash
sudo raspi-config

#password
#locale
#timezone
#hostname --> raspi-4b
#enable vnc
```

Also [set-up](https://github.com/essans/RasPi/blob/master/networking/vnc_setup.md) vnc access in case needed later.

<br>

(9) Install python in case not already installed, along with the [fabric package](http://www.fabfile.org) that I will need later.

```sh
sudo apt install python3-pip

sudo pip3 install fabric
```

and I'll install screen in case needed

```sh
sudo apt-get install screen
```


Basic set-up of the master node is now complete.

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


{wip}


















