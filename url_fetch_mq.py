#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: cyrusin
"""URL Fetching and Parsing Tool based on many threading queues
Include one queue used to hold the host name and
another queue used to hold the web page.

"""
import Queue
import threading
import time
import urllib2
from bs4 import BeautifulSoup

hosts = ["http://yahoo.com", \
            "http://google.com", \
            "http://baidu.com", \
            "http://apple.com"
            ]

url_queue = Queue.Queue()
page_queue = Queue.Queue()

class FetchUrlThread(threading.Thread):
    '''class ThreadUrl(threading.Thread)
    Thread used to fetch the url and put the page in another queue.

    '''
    def __init__(self, url_queue, page_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.page_queue = page_queue

    def run(self):
        while True:
            host = self.url_queue.get()
            url = urllib2.urlopen(host)
            chunk = url.read()
            self.page_queue.put(chunk)
            self.url_queue.task_done()


class DatamineThread(threading.Thread):
    '''DatamineThread(threading.Thread)
    Thread used to mine the webpage.

    '''

    def __init__(self, page_queue):
        threading.Thread.__init__(self)
        self.page_queue = page_queue

    def run(self):
        while True:
            chunk = self.page_queue.get()
            soup = BeautifulSoup(chunk)
            print soup.findAll(['title'])
            self.page_queue.task_done()

start = time.time()
def main():
    for i in range(4):
        fetch_thread = FetchUrlThread(url_queue, page_queue)
        fetch_thread.setDaemon(True)
        fetch_thread.start()

    for host in hosts:
        url_queue.put(host)

    for i in range(4):
        mine_thread = DatamineThread(page_queue)
        mine_thread.setDaemon(True)
        mine_thread.start()

    url_queue.join()
    page_queue.join()

main()
print "Elapsed time: %s" % (time.time() - start)
