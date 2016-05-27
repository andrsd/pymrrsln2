#!/usr/bin/env python2
#
# This script monitors messages on the LocoNet and prints them
#

from __future__ import print_function
import pymrrsln2
import argparse
import os
import time
import Queue

# default name of the config file
cfg_file = 'config'

# command line arguments
cmdline = argparse.ArgumentParser()
cmdline.add_argument("-c", "--config", help="Use config file")
cmdline.add_argument("--raw", help="Do not decode LocoNet messages, print them in raw format", action="store_true")
args = cmdline.parse_args()

def str_state(state):
  if state == pymrrsln2.LocoNet.SENSOR_HI:
    return "HI"
  elif state == pymrrsln2.LocoNet.SENSOR_LO:
    return "LO"
  else:
    return "Unknown"

def recv(msg):
  print(time.strftime("%H:%M:%S") + " : ", end='')
  if args.raw:
    print("RECV '" + " ".join("0x{:02x}".format(ord(c)) for c in msg['raw']) + "'")
  else:
    if msg['type'] == pymrrsln2.LocoNet.MSG_POWER_ON:
      print("Global power on")
    elif msg['type'] == pymrrsln2.LocoNet.MSG_POWER_OFF:
      print("Global power off")
    elif msg['type'] == pymrrsln2.LocoNet.MSG_SWITCH_STATE:
      print("Switch id = " + str(msg['id']) + ", state = " + str(msg['state']))
    elif msg['type'] == pymrrsln2.LocoNet.MSG_SENSOR_STATE:
      print("Sensor id = " + str(msg['id']) + ", state = " + str_state(msg['state']))
    else:
      print("Unknown message")


# user defined a custom config file
if args.config != None:
  cfg_file = args.config

if os.path.exists(cfg_file):
  # load the config file
  execfile(cfg_file)

  # loconet!
  if port['device'] == None:
    exit("ERROR: Need to specify device in your config file.")
  else:
    ln = pymrrsln2.LocoNet(port)
  ln.receiver_handler = recv
  ln.run()
else:
  exit("ERROR: config file '" + cfg_file + "' does not exist.")
