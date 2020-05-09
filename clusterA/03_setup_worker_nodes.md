### Worker node set-up and configuration

First power-up everything

#### Discover IP addresses for each node

(1) On the master-node:

```sh
sudo apt install nmap
```

On the master node find out the network range for the ethernet network just established using ```ifconfig``` and then scan that range.  Under ```eth0``` there shoud be an entry:

```inet 192.168.5.1  netmask 255.255.255.0  broadcast 192.168.5.255```

We are going to scan that range using CIDR notation.  For example ```192.168.5.0/24``` scans the 256 IP addresses from ```192.168.5.0``` to ```192.168.5.255```.  And, ```192.168.5.0/16``` would scan all 65,534 IP addresses from ```192.168.0.0``` to ```192.168.255.255```.  The first scan would take a few seconds while the latter would take 30-60minutes.

```sudo nmap -sn 192.168.5.0/24```

This will return a list of IP addresses active on our isolated network.

(2) Not necessary (indeed it would be impractical at scale and for remote servers) we can from the master-node, ssh into each pi and execute the following to "flash" the green LED:

```sh
sudo sh -c "echo 1 >/sys/class/leds/led0/brightness"
```

By convention we’ll assign node number from the top beginning with 1.  Note them down the configuration looks like this:

```sh
192.168.5.1 Master aka raspi-4b (also reachable via 192.168.1.186 on wlan0)

192.168.5.41
192.168.5.42
192.168.5.19
192.168.5.8
192.168.5.9
```
---
<br>

#### Configure each worker node

I need to upate/upgrade the OS on each node and make initial configuration changes.  I could take a number of approaches:

(a) ssh into each node and make these changes one at time.  Just about manageable task for 5 nodes, but what if I had 50 nodes?

(b) Make all changes on one of the nodes and then clone the card for each of the other 4.  Again a manageable task for 1+4 nodes, but what if I had 1+49 ?  What if the worker nodes are not in the same physical location?

(c) The approach I take is via the ```fabric``` python package which allows programatic scheduling and running of shell commands over ssh.  I can write some code that stores the IP addresses, user names, passwords etc for each node; loop across each of these node while passing the desired command lines we want to run. 

(1) On master-node create the ```~/code/python``` folder, then create a ```cluster_config.py``` file and copy/paste code from [here](https://github.com/essans/RasPi/blob/master/cluster/configure_cluster.py).  Run a ```chmod u+x``` and then:

```sh
./cluster_config.py --help
```
which will return:

```
execute command across cluster

optional arguments:
  -h, --help  show this help message and exit
  -v V        Verbose (default: Y)
  -c C        command to execute (default: 'hostname -I')
  -m M        include master node (default: N)
  -n N        node number (default: 99 for all)
```

Testing first using the following which should flash the green LED across each node:

```sh
./cluster_config.py -c 'sudo sh -c "echo 1 >/sys/class/leds/led0/brightness"' -m Y
```

(2) Once confirmed okay, then run an update and upgrade across all worker nodes:

```sh
./cluster_config.py -c 'sudo apt-get -y update'
```

```sh
./cluster_config.py -c 'sudo apt-get -y upgrade'
```

and then reboot:

```sh
./cluster_config.py -c 'sudo shutdown -r now’
```

(2) Check and update localization for each worker node:

```./cluster_config.py -c ‘timedatectl'``

Raspberry Pi boards usually ship with the UK localization so we’ll need to update if we’re (say) based in New York and the master is configured as such.  The following will list available timezones:

```timedatectl list-timezones```

```./cluster_config -c 'sudo timedatectl set-timezone America/New_York'```

and then check that the updates were made:

```./cluster_config.py -c ‘timedatectl'```

(3) Check and update locale settings:

```./cluster_config.py -c ‘locale'```

If update is needed, first check that the locale is available:

```./cluster_config.py -c ‘locale -a'```

If not then generate as needed.  In this case for en_US first uncomment it in the locale.gen file if necessary.

```sh
./cluster_config.py -c 'sudo sed -i "/en_US.UTF-8/s/^#[[:space:]]//g" /etc/locale.gen' -n 1

#removes ‘# ‘
#to recomment a line with a trailing space:
#sed -i '/<pattern>/s/^/# /g' file
```

```./cluster_config.py -c 'sudo locale-gen'```

```./cluster_config.py -c 'sudo update-locale LANG=en_US.UTF-8'```

and then check/confirm:

```./cluster_config.py -c 'locale'```

(4) Change passwords:
```.cluster_config.py -c 'echo -e "raspberry\nNewPassword\nNewPassword" | passwd'```

Now, update the new passwords in the ```cluster_config.py``` script.



