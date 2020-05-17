### Raspberry Pi VNC access

In the same way that SSH allows access to the command line of the raspberry pi,  VNC (Virtual Networking Computing) allows access to the GUI of the raspberry pi if/when needed.   

1) Enable VNC via ```sudo raspi-config``` if not already done.


2) Set a password via:

```
    sudo vncpasswd -service
    
    #should return "Successfully set password VNC parameter in /root/.vnc/config.d/vncserver-x11"
```

3) Create the following file with a single line:

```
    sudo nano /etc/vnc/config.d/common.custom
    
    Authentication=VncAuth
```

And then restart the vnc service:


```
sudo systemctl restart vncserver-x11-serviced
```

4) You may need to re-enable vnc via ```raspi-config``` and you may also need to install ```tightvncserver```. 

-----

When accessing the desktop UI remotely we first need to ``` sudo raspi-config``` and set resolution to something that makes sense depending on the client (usually the highest resolution for a mac) and also set ```boot to desktop```.

From a safari browser the navigate to:

```
vnc://192.168.1.184
```
