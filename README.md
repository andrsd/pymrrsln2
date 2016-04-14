pymrrsln2
==========

Two aspect signaling for model railroads using Digitrax LocoNet.


Dependencies
------------

* A machine that can run `python` and has USB port that can do serial communication, for example [Raspberry Pi Zero](https://www.raspberrypi.org/products/pi-zero/)
* [pyserial](https://pypi.python.org/pypi/pyserial)
* [Digitrax PR3XTRA](http://www.digitrax.com/products/computer-control/pr3xtra/)
* SE8c configured for signaling and all signals physically connected


Quick Setup
-----------

* Connect PR3XTRA to the computer using an USB cable
* Configure your signaling
* `python signals.py <signaling file>`
	- to exit, press `Ctrl + C`


Configuring Signals
-------------------

* Copy `config.example` to `config` and edit it.  It shows an example config for linux, Mac OS X, and Windows.

	On linux, it might look like:
	```
	port = {
	  'device'    : '/dev/ttyACM0',
	  'baud_rate' : 57600
	}
	```

* Copy `signals.example` to `signals` and edit it to match your layout.
	- For each detection block (indexed from one), you will need to specify what signal heads will go `GREEN` when a train enters the block (i.e. `SENSOR_HI`),
	and what signal heads will go `RED` when train leaves the block (i.e. `SENSOR_LO`).
	- Signal heads are also indexed from one, single SE8c can provide 32 heads.
	- Match the number of aspects in the signaling file to what ever your SE8c is set to
	- Simple example of the signaling file:
		```
		NUM_ASPECTS = 4

		SIGNALS = {
		  # block detection ID
		  2 : {
		    SENSOR_HI : {
		      # set signal head 4 and 16 to RED
		       4 : RED,
		      16 : RED
		    },
		    SENSOR_LO : {
		       4 : GREEN,
		      16 : GREEN
		    }
		  },
		}
		```
