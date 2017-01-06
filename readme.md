# Unifi NVR Client

This is a collection of python libraries and utilities
that I use to interact with a Ubiquiti NVR appliance.

The code is super rough and not very well documented.
I'll work on that.

`web/` contains a small Tornado webserver that enumerates
cameras and displays motion thumbnails for recent recordings
from them.

`py/NvrApi.py` is the main API for talking to the NVR.

`py/PhoneWatchdog.py` automatically turns recording on or off
for a set of cameras based on whether an iphone is found on
the local network.
