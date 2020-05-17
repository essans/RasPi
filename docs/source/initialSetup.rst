**************************
Raspberry Pi initial setup
**************************


Unless purchased in a "product bundle" raspberry-pi arrive as a single-board-computer.  Nothing else.  Each board requires:
  * Micro SD card (class 10, UHS-1 for faster speed.  16gb or 32gb)
  * Power supply (see `here <https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md>`_ )

Notice keyboard, mouse, monitor (and HDMI cable) are not listed here as the the raspberry Pi machines will mostly be operated "headless" which means access will be remote using ``ssh`` or ``vnc``.

-----

Flash Operating System to SD-card
=================================

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
============================

5) Login into the router portal via (eg) ``http://192.168.1.1`` in order to find determine which the IP address the router has assigned to the new device that is now connected to the network. Could also use a network scanner via the mac. Then ssh into the pi:

.. code-block:: bash

    ssh pi@192.168.1.168
    
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
^^^^^^^^^^^^^^^^^


