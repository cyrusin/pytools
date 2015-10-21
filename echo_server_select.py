#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''TCP echo server based on select
'''

import select
import socket
import Queue

#Init socket
listen_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setblocking(0)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind server
server_address = ('127.0.0.1', 8080)
listen_socket.bind(server_address)
listen_socket.listen(10)

#select轮询的sockets: 监听读事件
read_set = [listen_socket]

#监听写事件
write_set = []

#消息映射: connection : message queue
connect_to_msgq = dict()

#select超时
timeout = 10

#select IO复用处理连接
while True:
    readable, writeable, exceptional = select.select(read_set, write_set, read_set, timeout)
    if not (readable or writeable or exceptional):
        print u'本次select调用超时...'
        continue

    for s in readable:
        if s is listen_socket: #监听socket
            connection, client_addr = s.accept() #connection is the client socket obj 
            connection.setblocking(0)
            write_set.append(connection)
            connect_to_msgq[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print 'Get ', data, ' from client:', s.getpeername()
                connect_to_msgq[connection].put(data)
                if s not in write_set:
                    write_set.append(s)
            else: #连接已关闭
                print 'Close connection: ' + client_addr
                #读、写、消息队列将当前连接全部清楚
                if s in write_set:
                    write_set.remove(s)
                read_set.remove(s)
                s.close()
                connect_to_msgq.pop(s)

    for s in writeable:
        try:
            #队列的get()方法, 默认block为True, 即当队列为空, 线程阻塞
            #如果block为False, 则抛出Empty异常, 并不会阻塞当前进程
            #get_nowait()相当于block=False
            msg = connect_to_msgq[s].get_nowait()
        except Queue.Empty:
            print 'client: ' + s.getpeername() + 'msg queue is empty'
            write_set.remove(s)
        else:
            s.send(msg)

    for s in exceptional:
        print 'Exception in connection to client: ' + s.getpeername()
        read_set.remove(s)
        if s in write_set:
            write_set.remove(s)
        s.close()
        connect_to_msgq.pop(s)


