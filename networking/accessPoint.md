## Background
![raspi-4a](http://raspi.soobratty.com/github/raspi4a.jpeg)

For the past few months I've had a Raspberry Pi 4 (raspi-4a) connected to my home network via ethernet cable and it is constantly running which means I can connect to it using ssh from both within my network and also from outside using port forwarding.  I'm not using the default port 21 which means i no longer see attempted access from all parts of the globe.  At one point the attempted access was so frequent that I was [monitoring](https://github.com/essans/RasPi/tree/master/access) these attempts.

I also have a number of other Raspberry Pi boards that connect to my wifi router directly and i got thinking that maybe there'd be a way to route that traffic through the raspi-4a.  A little bit of research resulted in the raspi-4a now having the capability of being a wifi access point (when needed) using it's own ssid ("RASPI-NET").

It took quite a bit of trial and error as I wanted to the raspi-4a to continue functioning as a Raspberry Pi board with its own access to the internet via the ethernet connection.  These are the sequential steps that ultimately resulted in achieving this objective.

At the bottom of this note are the various sources of information used

