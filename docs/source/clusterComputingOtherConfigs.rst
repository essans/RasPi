====================
Other Configurations
====================


Disable red LEDs
----------------

As all nodes on the cluster will be accessed remotely and then shutdown remotely it is useful to confirm that everything has successfully powered down.  Visually this is not possible as the red LED remains on even after the machine has been shut-down.  But it is possible to disable the red LED while the Raspberry Pi is operational.  

This blog post from Jeff Geerling shows how:
https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi

------

Execute across cluster:

.. code-block:: bash

  ./cluster_serial_exec.py -c 'echo 0 | sudo tee /sys/class/leds/led1/brightness' -m
  

LED's will remain disabled unless turned back on by placing ``echo 1`` in the above, or upon shutdown.

------

Add useful commands as aliases to ``bashrc`` file
---------------------------------------------

.. code-block:: bash

  alias ledoff="echo 0 | sudo tee /sys/class/leds/led1/brightness"
  alias ledoff="echo 0 | sudo tee /sys/class/leds/led1/brightness"
  
  alias clustercmd="python3 ~/code/python/cluster/clustercmd"
  
We can also update the bashrc file on other nodes:

.. code-block:: bash

  clustercmd -c "echo ' ' >> ~/.bashrc
  
  clustercmd -c "echo 'alias ledoff=\"echo 0 | sudo tee /sys/class/leds/led1/brightness blah\"' >> ~/.bashrc
  
  clustercmd -c "echo 'alias ledon=\"echo 0 | sudo tee /sys/class/leds/led1/brightness blah\"' >> ~/.bashrc
  
