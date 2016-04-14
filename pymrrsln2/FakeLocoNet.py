from __future__ import print_function
import Queue
import os
import sys
import time
from LocoNet import LocoNet

"""
Class to fake LocoNet traffic
"""
class FakeLocoNet(LocoNet):
  def __init__(self, port):
    LocoNet.__init__(self, port)
    self.q = Queue.Queue()

    # read the data file
    with open(port['file']) as f:
      lines = f.readlines()

    for l in lines:
      idx = l.rfind('#')
      line = l[:idx]
      if (len(line) > 0):
        line = line.rstrip()
        str_bytes = line.split(' ')
        bytes = []
        for b in str_bytes:
          bytes.append(chr(int(b, 16)))
        n = len(bytes)
        self.q.put({ 'opcode' : bytes[0], 'data' : "".join(bytes[1:n-1]), 'checksum' : bytes[n - 1] })


  def receiver_thread(self):
    while not self.exit:
      if not self.q.empty():
        item = self.q.get()
        msg = self.decode(item['opcode'], item['data'], item['checksum'])
        self.msg_lock.acquire()
        self.msg_queue.put(msg)
        self.msg_lock.release()
        self.rd_event.set()
      time.sleep(0.1)
