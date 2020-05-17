==========================
Raspberry Pi initial setup
==========================

Unless purchased in a "product bundle" raspberry-pi arrive as a single-board-computer.  Nothing else.  Each board requires:

* Micro SD card (class 10, UHS-1 for faster speed.  16gb or 32gb)
   
* Power supply (see `here <https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md>`_ )

Note that akeyboard, mouse, HDMI cable, monitor are not listed here as the the raspberry Pi machines will mostly be operated "headless" which means access will be remote using Secure Shell (SSH) protocol or Virtual Network Computing (VNC).

-----

Flash Operating System to SD-card
---------------------------------

Most of the time the "Rasbian" operating system which is based on the debian linux distribution and provided by the Raspberry Pi Foundation works fine.

The Raspberry Pi Foundation now `provides <https://www.raspberrypi.org/documentation/installation/installing-images/>`_ a utility for choosing the OS and then imaging directly to the SD-Card.

Alternatively for a little more control:

1) Download and save in a folder the latest Rasbian images from `here <https://www.raspberrypi.org/downloads/raspbian/>`_.  At least one raspi should have the full version which include the GUI the OS and other software.  Likely though the lite version which does not come a GUI nor other softare will suffice as we'll be accessing from the command line over ssh. 
    
2) Flash the image onto an SD Card using `etcher <https://www.balena.io/etcher/>`_ for Mac OS. 

3) In the boot partition I create an empty file to enable ssh

.. code-block:: bash
    
    sudo diskutil mount /dev/disk2s1  #or whatever the boot partition is

    cd /volumes/boot

    touch ssh
    
4) Enable connection to wifi by creating a ``wpa_supplicant.conf`` file in the same boot partition and input following information:

.. code-block:: bash
    
    nano wpa_supplicant.conf
    
and in the file:    

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

5) First we need to access and login to the raspi over wifi:

   (i) Login into the router portal via (eg) ``http://192.168.1.1`` in order to find determine which the IP address the router has assigned to the new device that is now connected to the network. Could also use a network scanner via the mac. Then ssh into the pi:
   
   
       .. code-block:: bash
   
           ssh pi@192.168.1.186

    
   (ii) Alternatively, if the raspberry pi is the only one on the network (or at least the only one that is still has the default hostname ``raspberrypi`` then you can access more generically with:
 
        .. code-block:: bash
   
            ssh pi@raspberrypi.local
    
    
Update the OS and other programs

.. code-block::bash

    sudo apt-get update
    sudo apt-get upgrade
    
6) Likely not needed any more but to be on the safe side expand the file-system to take advantage of the SD-card capacity:

.. code-block:: bash

    sudo raspi-config --expand-rootfs
    
    
7) Update various configurations via command line via ``sudo raspi-config``:
   * password
   
   * set the locale
   
   * update timezone
   
   * set a hostname (eg rasp-4a)
   
   * enable vnc


8) Install any linux command-line utilities and programs as needed.  eg to install ``screen``

.. code-block:: bash

    sudo apt-get install screen
    

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



