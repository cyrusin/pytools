#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''Producer-Consumer problem
'''

import threading
import random
import Queue
import time

BUF_SIZE = 10
q = Queue.Queue(BUF_SIZE)


#producer
class Producer(threading.Thread):
    def __init__(self, name=None):
        super(Producer, self).__init__()
        self.name = name

    def run(self):
        while True:
            if not q.full():
                item = random.randint(1, 10)
                q.put(item)
                print self.name, " produce:", item
                time.sleep(random.random())


#consumer
class Consumer(threading.Thread):
    def __init__(self, name=None):
        super(Consumer, self).__init__()
        self.name = name

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                print self.name, " consume:", item
                time.sleep(random.random())


if __name__ == '__main__':
    p = Producer('producer')
    c = Consumer('consumer')

    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
