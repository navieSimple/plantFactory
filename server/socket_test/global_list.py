import Queue

SERVER_IP = "182.61.18.112"
SERVER_PORT = 50013
server_addr = (SERVER_IP, SERVER_PORT)

socket_tcp = None

threads = []

TCP_link_is_OK = 1 #1:link is OK; 0: link is broken

RcvData_MAX_len = 1024

g_queue_recv = Queue.Queue()
g_queue_send = Queue.Queue()

zone = 0 # 0: growth zone; 1: nursery zone
collector_zone_parameters = 0 # 1: collector get just zone parameters; 0: collector will get the parameters of the shelf.  

collector_ID ="AABBBCCCC" 
shelf_ID = {} #key is shelf_ID; value is the number of layer corresponding to shelf_ID
shelfID_to_collector_shelfID= {}#shelfID is corresponding to shelfID of collector
list_all_startandend_time_for_light = []#it is a two dimension.
                        #[[shelf_ID layer_ID light_type start_time end_time],...] 
list_all_light_status = [] ##it is a two dimension.
                        #[[shelf_ID layer_ID light_status ultraviolet_status],...] 
ini_start_time =730
ini_end_time =1930

waterlevel_low = 0
shelf_to_waterlevel = {1:1,2:1,3:1,4:1} # the waterlevel of each shelf is low or not.
#{shelf_num:0/1/2} 0: waterlevel is low; 1: waterlevel is ok; 2: waterlevel is high

trade_dict_data = {}

timer = None
heart_jump_time = 10

heart_jump_num = 0

waterdump_timer = None
waterdump_work_duration = 150
waterdump_NOwork_duration = 600
waterdump_flag = 0
