On the mac

```
ssh-keygen

ssh-copy-id pi@192.168.1.182  #ip address of host machine

cp id_rsa raspi4a  #rename key

rm id_rsa
rm id_rsa.pub
```
<br>

```
sudo chmod 600 raspi 4a
```

<br>

on RasPi:

```
sudo nano ~/etc/ssh/sshd_config
```

```
# change from 21 to something less obvious.  Mirror on router config

Port 21

PasswordAuthentication no

```
