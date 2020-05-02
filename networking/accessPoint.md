## Background
![raspi-4a](http://raspi.soobratty.com/github/raspi4a.jpeg)

For the past few months I've had a Raspberry Pi 4 (raspi-4a) connected to my home network via ethernet cable and running 24/7.  I can remote into the device using ssh from both within my local network and also from outside using port forwarding.  I'm not using the default port 21 which means i no longer see attempted access from all parts of the globe.  At one point the attempted access was so frequent that I was [monitoring](https://github.com/essans/RasPi/blob/master/networking/access_log.py) these attempts.

I also have other Raspberry Pi boards that connect to my wifi router directly and i got thinking that maybe there'd be a way to route that traffic through the raspi-4a.  A little bit of research resulted in the raspi-4a now having the capability of being a wifi access point (when needed) using it's own SSID ("RASPI-NET").

It took quite a bit of trial and error as I wanted to the raspi-4a to continue functioning as a Raspberry Pi board with its own access to the internet via the ethernet connection.  These are the sequential steps that ultimately resulted in achieving this objective.

At the bottom of this note are the various sources of information used.

***

### Steps to follow:

#### (1) Make sure system is updated:

```
sudo apt-get update
sudo apt-get upgrade
```

#### (2) Install 2 out of the 3 required packages:

```
sudo apt-get install hostapd   #package that lets us create a wireless hotspot
sudo apt-get install dnsmasq   #easy-to-use DHCP and DNS server
```

#### (3) We’re going to edit the programs’ configuration files in a moment, so let’s turn the programs off before we start tinkering:

```
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
```

#### (4) Edit the dhcpcd configuration file

```
sudo nano /etc/dhcpcd.conf
```

```
#These first two lines were added later after lots of trial and error. 
#Both are needed to ensure that the bridge works correctly.
#They stop the eth0 and wlan0 ports being allocated IP 
#addresses by the DHCP client on the Raspberry Pi

denyinterfaces wlan0    
denyinterfaces eth0     


#Next configure a static IP for the wlan0 interface

interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant


#static IP address to enable ssh and also accessing 
#the internet from the raspberry pi.
#This bit was discovered after some trial and error...

interface br0
static ip_address=192.168.1.184/24. <--- s
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
```

#### (5) Now restart the service

```
sudo service dhcpcd restart
```

#### (6) Edit this fine to configure the DHCP server

```
sudo nano /etc/dnsmasq.conf
```

...and add the following to the end of the file:

```
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h

```

The way to undersand this is that for ```wlano``` we are going to provide IP addresses between 192.168.4.2 and 192.168.4.20, with a lease time of 24 hours. If you are providing DHCP services for other network devices (e.g. eth0), you could add more sections with the appropriate interface header, with the range of addresses you intend to provide to that interface.

There are many more options for dnsmasq.  See [dnsmasq documentation](http://www.thekelleys.org.uk/dnsmasq/doc.html) for more details.

#### (7) Restart service

```
sudo systemctl start dnsmasq
```

#### (8) Configure the access point host software

```
sudo nano /etc/hostapd/hostapd.conf
```

```
interface=wlan0
#driver=nl80211
bridge=br0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=RASPI-NET
wpa_passphrase=<password_goes_here>
```

The commented out ```driver=nl80211``` would have been needed if using as stand-alone access point without bridge.

```hw_mode``` options:
>> To use the 5 GHz band, you can change the operations mode from hw_mode=g to hw_mode=a. Possible values for hw_mode are:

>> * a = IEEE 802.11a (5 GHz)
>> * b = IEEE 802.11b (2.4 GHz)
>> * g = IEEE 802.11g (2.4 GHz)
>> * ad = IEEE 802.11ad (60 GHz) (Not available on the Raspberry Pi)

#### (9) Now, edit the following file as we need to tell the system where to find the configuration file:

```
sudo nano /etc/default/hostapd
```

Find the line with #DAEMON_CONF, and replace it with this:

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

#### (10) Enable and start hostpad

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

and check status:

```
sudo systemctl status hostapd
sudo systemctl status dnsmasq
```

#### (11) Add routing and masquerade by first...

editing:

```
sudo nano /etc/sysctl.conf
```

and uncommenting and enabling:

```
net.ipv4.ip_forward=1
```

#### (12) and then, add a masquerade for outbound traffic on eth0:

```
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
```

#### (13) Save the iptables rule

```
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

#### (14) Edit the following file:

```
sudo nano /etc/rc.local
```

and add this just above “exit 0” to install these rules on boot:

```
iptables-restore < /etc/iptables.ipv4.nat
```

#### (15) Reboot

```
sudo reboot
```

***

Using a wireless device, search for networks.<br>

The network SSID specified in the ```hostapd``` configuration should discoverable, and it should be accessible with the specified password.

If SSH is enabled on the Raspberry Pi access point, it should be possible to connect to it as follows, assuming the pi account is present:

```
ssh pi@192.168.4.1
```

Rpi is is acting as an access point and other devices can associate with it.  Associated devices can access the raspberry pi access point via its IP address for operations such as “rsync”, “scp” or “ssh”.

***

### Using the Raspberry Pi as an access point to share an internet connection (bridge)

Now, I want to use raspi-4a as an access point to provide wireless internet access to other devices.  I also want the rasp-a to be able to access the internet via the ethernet connection.

To do this, a 'bridge' needs to put in place between the wireless device and the Ethernet device on the access point Raspberry Pi. This bridge will pass all traffic between the two interfaces. 

```
sudo apt install bridge-utils

sudo systemctl stop hostapd

sudo brctl addbr br0   #add the bridge

sudo brctl addif br0 eth0   #make the connection

```

Create a file in order to create a linux bridge (br0) and add a physical interface (eth0) to the bridge:

```
sudo nano /etc/systemd/network/bridge-br0.netdev
```

```
[NetDev]
Name=br0
Kind=bridge
```

Next, configure the bridge interface ```br0``` and the slave interface ```eth0``` using ```.network``` files as follows:

```
sudo nano /etc/systemd/network/bridge-br0-slave.network
```

```
[Match]
Name=eth0

[Network]
Bridge=br0
```

```
sudo nano /etc/systemd/network/bridge-br0.network
```

```
[Match]
Name=br0


[Network]
Address=192.168.10.100/24
Gateway=192.168.10.1
DNS=8.8.8.8
```

```
sudo systemctl restart systemd-networkd
```

We can also use the ```brctl``` tool to verify that a bridge ```br0``` has been created.  Next reboot and then:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

There should now be a functioning bridge between the wireless LAN and the Ethernet connection on the Raspberry Pi, and any device associated with the Raspberry Pi access point will act as if it is connected to the access point's wired Ethernet.
The bridge will have been allocated an IP address via the wired Ethernet's DHCP server. Do a quick check of the network interfaces configuration via:

```
ip addr
```
***


### References

https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/

https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

https://seravo.fi/2014/create-wireless-access-point-hostapd

https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/

http://raspberrypihq.com/how-to-turn-a-raspberry-pi-into-a-wifi-router/

https://www.instructables.com/id/Use-Raspberry-Pi-3-As-Router/

This might be interesting to explore one day….

https://imti.co/iot-wifi/
