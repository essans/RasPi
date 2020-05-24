==========================
Raspberry Pi initial setup
==========================

Unless purchased as part of a "product bundle" each raspberry-pi arrives as a single-board-computer.  Nothing else.  Each board requires:

* Micro SD card (class 10, UHS-1 for faster speed.  16gb or 32gb)
   
* Power supply (see `here <https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md>`_ )

* Optional: keyboard, mouse, monitor.

-----

Flash Operating System to the SD-card
-------------------------------------

The "Rasbian" operating system which is based on the debian linux distribution and provided by the Raspberry Pi Foundation works fine for most purposes.

The Raspberry Pi Foundation now `provides <https://www.raspberrypi.org/documentation/installation/installing-images/>`_ a utility for choosing the OS and then imaging directly to the SD-Card.  Alternatively for a little more control:

1) Download and save in a folder the latest Rasbian images from `here <https://www.raspberrypi.org/downloads/raspbian/>`_.  The full version includes a GUI for the OS and other software.  The lite version which does not come with a GUI nor other software will suffice when accessing the pi from the command line over ssh. 
    
2) Flash the image onto an SD Card using `etcher <https://www.balena.io/etcher/>`_ for Mac OS. 

3) In the boot partition create an empty file to enable ssh

   .. code-block:: bash

       sudo diskutil mount /dev/disk2s1  #or whatever the boot partition is

       cd /volumes/boot

       touch ssh
    
4) Enable connection to wifi by creating a ``wpa_supplicant.conf`` file in the same boot partition: 

   .. code-block:: bash

       nano wpa_supplicant.conf
    
and enter the following information:

   .. code-block:: bash

       ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
       update_config=1
       country=US

       network={
           ssid="NETWORK-NAME"
           psk="NETWORK-PASSWORD"
           key_mgmt=WPA-PSK
       }
    
Save the file and exit. Unmount and eject the SD card and insert into the Raspberry Pi and power on.


Additional OS configurations
----------------------------

1) Access and login to the raspi over wifi:

   * Login into the router portal (eg) ``http://192.168.1.1`` in order to determine which IP address the router has assigned to the new device that is now connected to the network. This can also be done using a network scanner. Then ssh into the pi:
   
   
    .. code-block:: bash

        ssh pi@192.168.1.186

    
   * Alternatively, if the raspberry pi is the only one on the network (or at least the only one that is still has the default hostname ``raspberrypi`` then you can access more generically with:
 
     .. code-block:: bash

         ssh pi@raspberrypi.local
    
    
Update the OS and other programs

   .. code-block::bash

       sudo apt-get update
       sudo apt-get upgrade
    
2) Likely not needed any more but to be on the safe side expand the file-system to take advantage of the SD-card capacity:

   .. code-block:: bash

       sudo raspi-config --expand-rootfs
    
    
3) Update various configurations via command line via ``sudo raspi-config``:

   * password
   
   * set the locale
   
   * update timezone
   
   * set a hostname (eg rasp-4a)
   
   * enable vnc
   
If the light version of the OS is installed or the raspi is *only* ever going to be used via the command-line as a headless device then the gpu memory allocation can be reduced to the 16mb minimum.  Set via ``advanced options`` in ``raspi-config``, or directly in the boot config file:

   .. code-block:: bash

      sudo nano /boot/config.txt
   
and add the following line at the bottom: ``gpu_mem=16``


4) Install any linux command-line utilities and programs as needed.  eg to install ``screen``, basic calculator ``bc`` etc.

   .. code-block:: bash

       sudo apt-get install screen
       sudo apt-get install bc
    
       
    
-----


Enable VNC access
-----------------

In the same way that SSH (Secure Shell) allows access to the command line of the raspberry pi,  VNC (Virtual Networking Computing) allows access to the GUI of the raspberry pi if/when needed.   

1) Enable VNC via ```sudo raspi-config``` if not already done.


2) Set a password via:

   .. code-block:: bash

       sudo vncpasswd -service

       #should return "Successfully set password VNC parameter in /root/.vnc/config.d/vncserver-x11"


3) Create the following file containing a single line:

   .. code-block:: bash

       sudo nano /etc/vnc/config.d/common.custom

       Authentication=VncAuth


Then restart the vnc service:

   .. code-block:: bash

      sudo systemctl restart vncserver-x11-serviced


4) You may need to re-enable vnc via ``raspi-config`` and you may also need to install and run ``tightvncserver``. 

-----

When accessing the desktop UI remotely we first need to ``sudo raspi-config`` and set resolution to something that makes sense depending on the client (usually the highest resolution for a mac) and also set ``boot to desktop``.

From a safari browser the navigate to ``vnc://192.168.1.184`` and enter password when prompted.

-----

SSH key and public key
----------------------

Access to the raspberry pi via SSH from within your network is usually safe, but if access is desired from outside the local network (ie internet) then a mere username + password combination may be vulnerable.

Security can be enhanced with the use of SSH key and public key for authentication.  More information on the SSH protocal, keys etc can be found `here. <https://www.ssh.com/ssh/>`_

1) In the home ``~``directory of the mac client machine generate the key, set a passphrase for the private key, and copy the public key to the pi

   .. code-block:: bash

      ssh-keygen

      ssh-copy-id pi@192.168.1.184
   
If the private key is likly to be one of many then rename it.  Delete the public key or achive it somewhere. 

   .. code-block:: bash

      mv id_rsa raspi4a

      rm id_rsa.pub
   
You may need to ``chmod 600 raspi4a``  for correct permissioning.
 
2) On the raspberry-pi server update various configuration by opening:

   .. code-block:: bash

      sudo nano /etc/ssh/sshd_config
   
Uncomment/enable ``PubkeyAuthentication yes``.  Set the ``Port`` number to match port-forwarding on the router, and make sure enable ``PasswordAuthentication no``.

3) Log-in to the network router/switch and enable port-fowarding with the port number (avoid the common Port 22...) mapped to the raspberry pi.

4) Restart the service with :class:`sudo service ssh restart`

5) Confirm that the selected port is listerning: :class:`netstat -tnl`

