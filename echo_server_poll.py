#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''tcp echo server based on select.poll
'''

import select
import socket
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
listen_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setblocking(0)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind server
server_address = (host, int(port))
listen_socket.bind(server_address)
listen_socket.listen(10)

#client message queue map
cli_msg_q = dict()

#超时时间, 毫秒
timeout = 5000

#读事件
READ_ONLY = (select.POLLIN|select.POLLERR|select.POLLPRI|select.POLLHUP)

#写事件
READ_WRITE = (select.POLLOUT|READ_ONLY)

#在监听socket上初始化poll对象
poller = select.poll()
poller.register(listen_socket, READ_ONLY)

#poll会返回(fd, event), 需要将fd映射到socket
fd_to_sock = {listen_socket.fileno(): listen_socket}

while True:
    print 'Waiting for connection...'
    #active_list: [(fd, event)...]
    active_list = poller.poll(timeout)
    if not active_list:
        print 'Poll timeout, poll again...'
        continue
    print 'Get ', len(active_list), ' events to process'
    for fd, event in active_list:
        sock = fd_to_sock[fd]
        if event & (select.POLLIN|select.POLLPRI):
            if sock is listen_socket:
                connection, client_addr = listen_socket.accept()
                print 'New connection: ', client_addr
                connection.setblocking(0)
                fd_to_sock[connection.fileno()] = connection
                poller.register(connection, READ_ONLY)
                cli_msg_q[connection] = Queue.Queue()
            else:
                data = sock.recv(1024)
                if data:
                    data = data.strip()
                    if data == 'EOF':
                        print 'Close connection to client: ', sock.getpeername(), '(EOF)'
                        poller.unregister(sock)
                        sock.close()
                        cli_msg_q.pop(sock)
                    else:
                        print 'Get data: ', data, 'from client: ', sock.getpeername()
                        cli_msg_q[sock].put(data)
                        poller.modify(sock, READ_WRITE)
                else:
                    print 'Close connection to client: ', sock.getpeername()
                    poller.unregister(sock)
                    sock.close()
                    cli_msg_q.pop(sock)
        elif event & select.POLLHUP: #连接关闭
            print 'Close connection to client: ', sock.getpeername(), '(HUP)'
            poller.unregister(sock)
            sock.close()
        elif event & select.POLLOUT: #写事件
            try:
                msg = cli_msg_q[sock].get_nowait()
            except Queue.Empty:
                print sock.getpeername(), 'queue is empty'
                poller.modify(sock, READ_ONLY)
            else:
                print 'Send', msg, ' to ', sock.getpeername()
                sock.send(msg+'\r\n')
        elif event & select.POLLERR:
            print 'Exception in connection to client: ', sock.getpeername()
            poller.unregister(sock)
            sock.close()
            cli_msg_q.pop(sock)

            
