=================
Cluster Computing
=================

Overview
--------

This recipe documets the steps taken in setting-up a cluster of Raspberry Pis.  The idea is to try a few different approaches and in doing so reinforce understanding of some of the principles relating to linux networking, distributed computing and a few other things...

-----

Architecture/Framework
^^^^^^^^^^^^^^^^^^^^^^
The architecture for this first cluster will comprise of 5 Raspberry Pi 3 Model B+ worker nodes, powered by a USB power supply unit and networked together via a simple unmanaged switch. The master node will be a Raspberry Pi 4 (4gb RAM) on a separate power-supply wired into the same network switch.

The master node will connect to the internet via wireless LAN and using "IP Masquerading" will provide gateway access to the internet for the worker nodes only when needed.

Operating system on master and worker nodes will be Raspbian/Debian flavour of linux.

-----

**Schematic**

.. image:: images/raspi_cluster_diagram_v1.png
    :align: center
    :alt: cluster

-----

**Parts List**

+-----+-----+-----+-----+
| Quantity | Part | Source | Cost |
+=====+=====+=====+=====+
| 1 | Raspberry Pi 4 (4gb) | [Canakit](https://www.canakit.com/raspberry-pi-4-4gb.html) | $ 55 |
+-----+-----+-----+-----+
| 5 | Raspberry Pi 3 Model B+ | [Canakit](https://www.canakit.com/raspberry-pi-3-model-b-plus.html) | $ 175 |
+-----+-----+-----+-----+
| 5 | Cat5e 1ft Ethernet patch cable| [Amazon](https://www.amazon.com/gp/product/B00JULVRU2/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&th=1) | $ 8 |
+-----+-----+-----+-----+
| 1 | Cat6 18in Ethernet patch cable| [Amazon](https://www.amazon.com/gp/product/B00E9RA6GI/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1) | $5 |
+-----+-----+-----+-----+
| 1 | GeauxRobot 6 layer dog bone stack | [Amazon](https://www.amazon.com/gp/product/B01D9130QC/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1) | $ 32 |
+-----+-----+-----+-----+
| 1 | Clear Case for Raspberry Pi 4 | [Amazon](https://www.amazon.com/gp/product/B07W72KL1W/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1) | $ 5 |
+-----+-----+-----+-----+
| 1 | Anker 60W PowerPort 6 6-port wall charger (2.4A per port max) | [Amazon](https://www.amazon.com/gp/product/B014T3ZJX6/ref=ppx_od_dt_b_asin_title_s01?ie=UTF8&psc=1) | $30 |
+-----+-----+-----+-----+
| 6 | Sabrent 22AWG 1ft micro USB to USB cables | [Amazon](https://www.amazon.com/gp/product/B014T3ZJX6/ref=ppx_od_dt_b_asin_title_s01?ie=UTF8&psc=1) | $ 8 |
+-----+-----+-----+-----+
| 1 | 15W (5v, 3A) power supply (Raspi 4) | [Pi Shop](https://www.pishop.us/product/raspberry-pi-15w-power-supply-us-white/) | $ 8 |
+-----+-----+-----+-----+
| 1 | NETGEAR 8-Port Gigabit Ethernet Unmanaged Switch | [Amazon](https://www.amazon.com/gp/product/B00KFD0SYK/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) | $ 22 |
+-----+-----+-----+-----+
| 1 | Powerstrip with independent switches | [Amazon](https://www.amazon.com/gp/product/B0775V2SS1/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) | $ 20 |
+-----+-----+-----+-----+
| 6 | SanDisk 32GB MicroSD HC ultra 80mb/s (non A1) | [Amazon](https://www.amazon.com/gp/product/B00CNYV942/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1) | $ 36 |
+-----+-----+-----+-----+
| | | | **$ 404**
+-----+-----+-----+-----+
