====================
Other Configurations
====================


Disable red LEDs
----------------

As all nodes on the cluster will be accessed remotely and then shutdown remotely it is useful to confirm that everything has successfully powered down.  Visually this is not possible as the red LED remains on even after the machine has been shut-down.  But it is possible to disable the red LED while the Raspberry Pi is operational.  

This blog from Jeff Geerling shows how:
https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi

Execute across cluster:

.. code-block:: bash

  ./cluster_config.py -c 'echo 0 | sudo tee /sys/class/leds/led1/brightness' -m y
  

LED's will remain disabled unless turned back on by placing ``echo 1`` in the above, or upon shutdown.
