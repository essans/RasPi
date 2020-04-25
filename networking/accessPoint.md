## Background
![raspi-4a](http://raspi.soobratty.com/github/raspi4a.jpeg)

For the past few months I've had a Raspberry Pi 4 (raspi-4a) connected to my home network via ethernet cable and it is constantly running which means I can connect to it using ssh from both within my network and also from outside using port forwarding.  I'm not using the default port 21 which means i no longer see attempted access from all parts of the globe.  At one point the attempted access was so frequent that I was [monitoring](https://github.com/essans/RasPi/tree/master/access) these attempts.

I also have a number of other Raspberry Pi boards that connect to my wifi router directly and i got thinking that maybe there'd be a way to route that traffic through the raspi-4a.  A little bit of research resulted in the raspi-4a now having the capability of being a wifi access point (when needed) using it's own ssid ("RASPI-NET").

It took quite a bit of trial and error as I wanted to the raspi-4a to continue functioning as a Raspberry Pi board with its own access to the internet via the ethernet connection.  These are the sequential steps that ultimately resulted in achieving this objective.

At the bottom of this note are the various sources of information used

***

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

#### (4) Configure static IP addresses for the wlan0 and eth0 interfaces
It is the bridge (which will be created later) that is the network device.  So we need to stop the eth0 and wlan0ports being allocated IP addresses by the DHCP #client on the Raspberry Pi.

```
denyinterfaces wlan0    #These two lines were added later after lots of trial and error 
denyinterfaces eth0     #Both are needed to ensure that the bridge works correctly


interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant


# static IP address to enable ssh and also accessing inet fro pi
# this bit was discovered after some trial and error

interface br0
static ip_address=192.168.1.184/24. <--- s
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
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
