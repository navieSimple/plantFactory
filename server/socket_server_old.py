import socket
import time
import sys
import global_list
import logging
#import my_log

def socket_init(): 
    HOST_IP = ""
    HOST_PORT = 50011
    
     
    print("Starting socket: TCP...")
    host_addr = (HOST_IP, HOST_PORT)
    global_list.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
    
    
    global_list.socket_tcp.bind(host_addr)
    global_list.socket_tcp.listen(1)   
     
    global_list.socket_con, (client_ip, client_port) = global_list.socket_tcp.accept()
    
    print("Connection accepted from %s." %client_ip)
    logging.info('Connection accepted from %s.', client_ip)
    #socket_con.send("Welcome to RPi TCP server!")
    
    print("Receiving package...")
    
def thread_recv():
    while True:
        data = global_list.socket_con.recv(512)
        if len(data)>0:
            logging.info('Received data: %s',data)
            global_list.g_queue_recv.put(data)

def thread_send():
    while True:
        while not global_list.g_queue_send.empty():
            data = global_list.g_queue_send.get()
            logging.info('Sent data: %s',data)
            global_list.socket_con.sendall(data)


'''            
def thread_send():
    while True:
        try:
            data = global_list.socket_con.recv(global_list.RcvData_MAX_len) 
            
            if len(data)>0: 
                print("Received: %s" %data)
                global_list.socket_con.send("OK!")
                time.sleep(1)
                continue
        except Exception:  
            global_list.socket_tcp.close()
            sys.exit(1)
'''