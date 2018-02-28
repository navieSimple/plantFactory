#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import select
import Queue

#create socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#set IP address reused
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#IP address and port number
server_address = ("", 50013)
#bind IP address
serversocket.bind(server_address)
#listening, and set max connect 
serversocket.listen(10)
print  "server start success,listenning IP:" , server_address
#set as non-block at server
serversocket.setblocking(False)  
#set timeout
timeout = 10
#create epoll event object,and subsequent events will be added in it
epoll = select.epoll()
#register server monitoring fd
epoll.register(serversocket.fileno(), select.EPOLLIN)
#save message dictionary from client. format is {}
message_queues = {}
#file handle is corresponding to object dictionary, format is {handle:object}
fd_to_socket = {serversocket.fileno():serversocket,}

print serversocket.fileno(),":",serversocket

while True:
  print "waiting active connect......."
  #epoll event aggregation registered ,return is [(file handle,corresponding event),(...),...]
  events = epoll.poll(timeout)
  if not events:
     print "epoll time out no active connect,re-poll......"
     continue
  print "have" ,len(events), "new event, start address......"
  
  for fd, event in events:
     socket = fd_to_socket[fd]
     print fd,event
     #if active socket is current server socket, it means that there is new connecton
     if socket == serversocket:
            connection, address = serversocket.accept()
            print "new connect:" , address
            #new socket connection is set as non-block
            connection.setblocking(False)
            
            #register new connection into event aggregation
            epoll.register(connection.fileno(), select.EPOLLIN)
            
            #save new file handle and object into dictionary
            fd_to_socket[connection.fileno()] = connection
            #new connection act as key value that is saved into queue, and save each connection information
            message_queues[connection]  = Queue.Queue()
     #close event
     elif event & select.EPOLLHUP:
        print 'client close'
        #unregister client file handle in the epoll
        epoll.unregister(fd)
        #close client file handle
        fd_to_socket[fd].close()
        #delete closed client related information in the dictionary
        del fd_to_socket[fd]
     #read event(select.EPOLLIN=1)
     elif event & select.EPOLLIN:
        #recieve data
        data = socket.recv(1024)
        if data:
           print "recieved data:" , data , "client:" , socket.getpeername()
           #put data into the corresponding client dictionary 
           message_queues[socket].put(data)
           #modify connection read 
           epoll.modify(fd, select.EPOLLOUT)
     #write event
     elif event & select.EPOLLOUT:
        try:
           #get corresponding client information from dictionary
           msg = message_queues[socket].get_nowait()
        except Queue.Empty:
           print socket.getpeername() , " queue empty"
           #modify file handle for read event
           epoll.modify(fd, select.EPOLLIN)
        else :
           print "sent data:" , data , "client:" , socket.getpeername()
           #send data
           socket.send(msg)

#unregister server file handle in the epoll
epoll.unregister(serversocket.fileno())
# close epoll
epoll.close()
#close server socket
serversocket.close()

