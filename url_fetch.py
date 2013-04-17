#!/usr/bin/env python
# -*- coding:utf8 -*-
#@Author: cyrusin
"""Url Fetch Tool based on multi-threading.

"""
import threading
import time
import urllib2
import Queue

hosts = ["http://yahoo.com", \
            "http://google.com", \
            "http://amazon.com", \
            "http://ibm.com", \
            "http://apple.com"]

queue = Queue.Queue()
class ThreadUrl(threading.Thread):
    """class ThreadUrl(threading.Thread)

    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):              
        """run(self): overriding the run() method of threading.Thread class.

        """
        while True:
            host = self.queue.get()
            url = urllib2.urlopen(host)
            print url.read(1024)
            self.queue.task_done()

start = time.time()
def main():
    for i in range(5):
        thread = ThreadUrl(queue)
        thread.setDaemon(True)
        thread.start()
        
    for host in hosts:
        queue.put(host)
    queue.join()

main()
print "Elapsed Time: %s" % (time.time() - start)
