#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import select
import sys
import Queue

if len(sys.argv) != 2:
    print "usage: python echo_server_poll.py 127.0.0.1:8080"

try:
    host, port = sys.argv[1].split(':')
except Exception, e:
    print e
    sys.exit(-1)

#Init socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setblocking(0)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind socket
server_address = (host, int(port))
listen_socket.bind(server_address)
print 'Echo server bind to ', server_address
listen_socket.listen(10)

#Epoll config
epoll_timeout = 10 #seconds

epoll = select.epoll()
print 'Epoll Init sucsess...'
epoll.register(listen_socket, select.EPOLLIN)
print 'Register ', 'fd: ', listen_socket.fileno(), ' event: EPOLLIN' 

#fd => socket obj
fd_to_sock = {listen_socket.fileno(): listen_socket,}

#Client_socket: msg_queue map
cli_msg_q = dict()

#main logic
while True:
    print 'Epoll start, waiting for connection...'

    #Epoll will return list of (fd, events)
    fd_events_list = epoll.poll(epoll_timeout)

    if not fd_events_list:
        print 'No events happend, just epoll again...'
        continue

    print 'Get', len(fd_events_list), ' events need to be processed'
    for fd, events in fd_events_list:
        sock = fd_to_sock[fd]
        if events & select.EPOLLIN:
            #Listen socket
            if sock is listen_socket:
                connection, client_addr = listen_socket.accept()
                print 'New connection from ', client_addr
                connection.setblocking(0)
                fd_to_sock[connection.fileno()] = connection
                cli_msg_q[connection] = Queue.Queue()
                epoll.register(connection, select.EPOLLIN)
            else: #Read from client socket
                raw_data = sock.recv(1024)
                if raw_data:
                    request = raw_data.strip()
                    if request == 'End':
                        print 'Close connection with client: ', sock.getpeername()
                        epoll.unregister(sock)
                        sock.close()
                        cli_msg_q.pop(sock)
                    else:
                        print 'Client: ', sock.getpeername(), 'said: ', request
                        cli_msg_q[sock].put(request)
                        epoll.modify(sock, select.EPOLLOUT)
                else:
                        print 'Close connection with client: ', sock.getpeername()
                        epoll.unregister(sock)
                        sock.close()
                        cli_msg_q.pop(sock)
        elif events & select.EPOLLOUT:
            try:
                response = cli_msg_q[sock].get_nowait()
            except Queue.Empty:
                print 'Queue of Client: ', sock.getpeername(), 'is Empty'
                epoll.modify(sock, select.EPOLLIN)
            else:
                print 'Send ', response, 'to client: ', sock.getpeername()
                sock.send(response+'\r\n')
        elif events & select.EPOLLHUP:
            print 'Close connection with client: ', sock.getpeername()
            epoll.unregister(sock)
            sock.close()
            cli_msg_q.pop(sock)


