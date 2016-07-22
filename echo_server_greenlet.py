#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''Echo server based on greenlet
'''
import collections
import functools
import socket
import sys
from select import select
import greenlet

if len(sys.argv) != 2:
    print "Usage: python echo_server_greenlet.py 127.0.0.1:8080"

try:
    host, port = sys.argv[1].split(':')
except Exception, e:
    print e
    sys.exit(-1)

grn_tasks = collections.deque()
recv_wait = {}
send_wait = {}


def main_loop():
    while any([grn_tasks, recv_wait, send_wait]):
        while not grn_tasks:
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                grn_tasks.append(('grn_r', recv_wait.pop(s)))
            for s in can_send:
                grn_tasks.append(('grn_r', send_wait.pop(s)))

        g_state, g_task = grn_tasks.popleft()
        if g_state == 'grn_r': # greenlet is active, just switch to it
            try:
                if g_task.dead:
                    continue
                sw_signal, sw_what = g_task.switch()
                if sw_signal == 'ev_recv':
                    recv_wait[sw_what] = g_task
                elif sw_signal == 'ev_send':
                    send_wait[sw_what] = g_task
            except Exception:
                continue
        elif g_state == 'grn_n': # init task in new greenlet
            grn_tasks.append(('grn_r', greenlet.greenlet(g_task)))


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

# Init first greenlet for server
client_handler = functools.partial(handle_client, echo_handler)
server_task = functools.partial(server, (host, int(port)), client_handler)
grn_server = greenlet.greenlet(server_task)

grn_tasks.append(('grn_r', grn_server))
main_loop()
