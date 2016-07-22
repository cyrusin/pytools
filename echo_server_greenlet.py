#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''Echo server based on greenlet
'''
import collections
import functools
import socket
import greenlet

grn_tasks = collections.deque()

def server(host_address, handle_client):
    '''start a server on host_address
    @host_address: tuple of `(ip, port)`
    @handle_client: function used to handle client request
    '''
    grn_current = greenlet.getcurrent()
    grn_parent = grn_current.parent #main greenlet

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(host_address)
    sock.listen(5)
    print "server listen on ", host_address

    while True:
        grn_parent.switch(('ev_recv', sock)) #switch to main greenlet
        client, addr = sock.accept() #blocking
        print "Connection", addr
        task = functools.partial(handle_client, client)
        grn_tasks.append(('grn_n', task)) #raw task
