[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://andrsd.mit-license.org/)

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
	- For each detection block (indexed from zero), you will need to specify a list of heads that guard this block
	- Signal heads are also indexed from zero, single SE8c can provide 32 heads.
	- Match the number of aspects in the signaling file to what ever your SE8c is set to
	- Simple example of the signaling file:
		```
		NUM_ASPECTS = 4

		SIGNALS = {
		  2 : [ 4, 16 ]
		}
		```
* If you want to find out the block IDs that go into your `signals` file, run the script with `--debug 1`. Then place a locomotive
  on your layout into a detection block and you should see a message like:
	```
	Block 0 , state = HI
	```
  When you remove the locomotive, you should see:
	```
	Block 0 , state = LO
	```

* To find out the signal head IDs.
	- For a single SE8c in default configuration, the switch IDs that control the signals start form 257, i.e. if you throw
	  or close switch 257 (and there is a signal head connected there), you should see the aspect changing.
	- If you know the switch ID, then use this formula:
		```
		head ID = (switch_ID - 257) / 2
		```
		Round the number down.
	- Then `head ID` goes into the `signals` file.


Monitoring LocoNet
------------------

If you want to monitor the messages on LocoNet, you can use the `monitor.py` script. You can see the raw messages if you run it with `--raw` flag. This can
serve as verification that your setup and serial connection works correctly before you run `signals.py`.
