#!/usr/bin/env python
# -*- coding:utf8 -*-
#@Author: cyrusin
import threading
import time
import urllib2

hosts = ["http://yahoo.com", \
            "http://google.com", \
            "http://amazon.com", \
            "http://ibm.com", \
            "http://apple.com"]
start = time.time()

for host in hosts:
    url = urllib2.urlopen(host)
    print url.read(1024)

print "Elapsed Time: %s" % (time.time() - start)
