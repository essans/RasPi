### Raspberry Pi VNC access

```
sudo raspi-config

---> enable VNC
```

<br>

```
sudo vncpasswd -service 

# Successfully set "Password" VNC parameter in /root/.vnc/config.d/vncserver-x11 
```

```
sudo nano /etc/vnc/config.d/common.custom
```

add the following line:
```
Authentication=VncAuth
```

```
sudo systemctl restart vncserver-x11-serviced
```

To monitor logs:

```
sudo journalctl -u vncserver-x11-serviced.service
```

---

When needing to access the desktop UI remotely we first need to ``` sudo raspi-config``` and set resolution to something that makes sense and also set ```boot to desktop```, and then reboot.

From a safari browser the navigate to:

```
vnc://192.168.1.184
```



Following might be needed:

```
sudo apt-install tightvncserver
```

After done with VNC access we then need to change back the ```raspi-config``` settings.


