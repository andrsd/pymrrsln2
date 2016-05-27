#!/usr/bin/env python2

from __future__ import print_function
import pymrrsln2
import argparse
import sys
import os
import time
import Queue

# default name of the config file
cfg_file = 'config'

# command line arguments
cmdline = argparse.ArgumentParser()
cmdline.add_argument("-c", "--config", help="Use config file")
cmdline.add_argument("--debug", help="Print debugging messages")
cmdline.add_argument("signaling_file", help="File that describes signaling")
args = cmdline.parse_args()

'''
Set the aspect on a signal head

@param head_id Signal head ID to be changed (0-based indexing)
@param aspect New aspect to be set
'''
def set_aspect(head_id, aspect):
  # get the switch ID
  sid = 257 + (head_id * NUM_ASPECTS / 2)

  if (NUM_ASPECTS == 2):
    # 2 aspect signaling
    if aspect == pymrrsln2.LocoNet.SIGNAL_GREEN:
      state = pymrrsln2.LocoNet.SWITCH_CLOSED
    elif aspect == pymrrsln2.LocoNet.SIGNAL_RED:
      state = pymrrsln2.LocoNet.SWITCH_THROWN
    ln.set_switch_state(sid, state)
  elif (NUM_ASPECTS == 4):
    # 4 aspect signaling
    if aspect == pymrrsln2.LocoNet.SIGNAL_GREEN:
      state1 = pymrrsln2.LocoNet.SWITCH_CLOSED
      state2 = pymrrsln2.LocoNet.SWITCH_CLOSED
    elif aspect == pymrrsln2.LocoNet.SIGNAL_RED:
      state1 = pymrrsln2.LocoNet.SWITCH_THROWN
      state2 = pymrrsln2.LocoNet.SWITCH_CLOSED
    elif aspect == pymrrsln2.LocoNet.SIGNAL_YELLOW:
      state1 = pymrrsln2.LocoNet.SWITCH_CLOSED
      state2 = pymrrsln2.LocoNet.SWITCH_THROWN
    elif aspect == pymrrsln2.LocoNet.SIGNAL_FLASHING_YELLOW:
      state1 = pymrrsln2.LocoNet.SWITCH_THROWN
      state2 = pymrrsln2.LocoNet.SWITCH_THROWN
    ln.set_switch_state(sid + 0, state1)

'''
Use the signal definition to set the signal heads

@param blk_id Block ID whose occupancy status was changed (zero-base indexing)
@param sensor_state Reported state of the occupancy (HI for occupied, LO for not occupied)
'''
def do_signaling(blk_id, sensor_state):
  if (blk_id) in SIGNALS:
    if sensor_state == pymrrsln2.LocoNet.SENSOR_LO:
      aspect = pymrrsln2.LocoNet.SIGNAL_GREEN
    else:
      aspect = pymrrsln2.LocoNet.SIGNAL_RED

    heads = SIGNALS[blk_id]
    for h in heads:
      set_aspect(h, aspect)

'''
Receiver callback

@param msg The decoded LocoNet message
'''
def recv(msg):
  # block occupancy change?
  if msg['type'] == pymrrsln2.LocoNet.MSG_SENSOR_STATE:
    #ln.set_switch_state(285, pymrrsln2.LocoNet.SWITCH_THROWN) 
    # do we have signaling definition?
    if 'SIGNALS' in globals():
      do_signaling(msg['id'], msg['state'])


# user defined a custom config file
if args.config != None:
  cfg_file = args.config

if os.path.exists(cfg_file):
  # load the config file
  execfile(cfg_file)
  if 'device' in port:
    # loconet!
    if port['device'] == None:
      ln = pymrrsln2.FakeLocoNet(port)
    else:
      ln = pymrrsln2.LocoNet(port)

    # process the file
    with open(args.signaling_file) as f:
      signaling = f.read()
      # replace signal aspects
      signaling = signaling.replace("RED", "pymrrsln2.LocoNet.SIGNAL_RED")
      signaling = signaling.replace("GREEN", "pymrrsln2.LocoNet.SIGNAL_GREEN")
      signaling = signaling.replace("YELLOW", "pymrrsln2.LocoNet.SIGNAL_YELLOW")
      signaling = signaling.replace("FLASHING_YELLOW", "pymrrsln2.LocoNet.SIGNAL_FLASHING_YELLOW")
      # replace sensor states
      signaling = signaling.replace("SENSOR_HI", "pymrrsln2.LocoNet.SENSOR_HI")
      signaling = signaling.replace("SENSOR_LO", "pymrrsln2.LocoNet.SENSOR_LO")
      exec(signaling)

    ln.receiver_handler = recv
    ln.run()
  else:
    print("ERROR: 'device' was not specified in the config file '" + cfg_file + "'.", file=sys.stderr)
else:
  print("ERROR: config file '" + cfg_file + "' does not exist.", file=sys.stderr)
