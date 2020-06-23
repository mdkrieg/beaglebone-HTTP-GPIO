# beaglebone-HTTP-GPIO
Provides access to beaglebone GPIO directly via HTTP.
Offers maximal flexibility but minimal security.

Tested on image "AM3358 Debian 10.3 2020-04-06 4GB SD IoT" from https://beagleboard.org/latest-images using "BeagleBone Black" and "BeagleBone Black Wireless"


# Installation and Use

Requires Adafruit_BBIO
```
pip install Adafruit_BBIO
```

Launch server with Python 3
```
python3 _server.py 
```

Example request to read state of all pins
```
/_fetch?cmd=allPins
```
* Returns JSON response of all configured pins

Example request to set state of a pin
```
/_do?pin=P8_12&cmd=setState&state=1
```
* Sets pin P8_12 to ON
* Returns JSON response of specified pin's new state


# To Do
* Come up with a better way to configure IO, currently all active pins have to be hard coded into the server script.
* Finish integrating the "simulator.html" template, originally provided in the OOB files.
