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


def handle_client(handle_request, client):
    '''handle client request using request_handler
    @client: client socket object
    '''
    error = False
    grn_current = greenlet.getcurrent()
    grn_parent = grn_current.parent
    while True:
        grn_parent.switch(('ev_recv', client))
        try:
            req = client.recv(100)
        except Exception:
            client.close()
            break
        if not req: #client has closed
            break
        try:
            resp = handle_request(req)
        except Exception:
            resp = b'Error in server\n'
            error = True
        grn_parent.switch(('ev_send', client))
        client.send(resp)
        if error:
            client.close()
            break
    print 'closed'


def echo_handler(req):
    return req + b'\n'

