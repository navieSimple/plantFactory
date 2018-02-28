import json_client
import datetime
from threading import Timer
import json

dict_data = {}
#a = {'fun_ID':'06', 'collector_ID':'231110001', 'layer_ID':'0001','water_level':'12.34', 'water_temp':'45', 'illumination':'123.5' }
#a = {'fun_ID':'07','collector_ID':'xx','shelf_ID':{'shelf_ID_1':'X','shelf_ID_2':'X'},'layer_ID':{'layer_ID_1':'B','layer_ID_2':'C'}}
a = {'fun_ID':'07','collector_ID':'231110001','shelf_ID':{ 'shelf_ID_1':'1','shelf_ID_2':'2','shelf_ID_3':'3','shelf_ID_4':'4' },'layer_ID': {'layer_num_1':'3','layer_num_2':'4','layer_num_3':'5','layer_num_4':'6' }}
dd = {'fun_ID':'02','collector_ID':'xx','shelf_ID':'xx','layer_ID_1':{ 'light':{ 'start_time':'xxxx','end_time':'xxxx'},'ultraviolet':{'start_time':'xxxx','end_time':'xxxx'}},'layer_ID_2':{ 'light':{'start_time':'xxxx','end_time':'xxxx'},'ultraviolet':{ 'start_time':'xxxx','end_time':'xxxx'}},'layer_ID_3':{'light':{'start_time':'xxxx','end_time':'xxxx'},'ultraviolet':{'start_time':'xxxx','end_time':'xxxx'}}}
#dddd = {'fun_ID':'02','layer_ID_1':{'light':{'start_time':'xxxx','end_time':'xxxx'}}
ddd = {'fun_ID':'02','layer_ID_1':'dd'}

b = json_client.json_encode(a)
print b

c = json_client.json_decode(b)
print c,len(c)
#print c['water_temp']
print c['shelf_ID']['shelf_ID_1']
print int(c['shelf_ID']['shelf_ID_1'])

print len(c)
print len(c['shelf_ID'])

num = 5
shelf_ID_key = 'shelf_ID_'+str(num)
shelf_ID_value = str(num)
c['shelf_ID'][shelf_ID_key] = shelf_ID_value

for key,value in c.items():
    print key,value
    
#File operation
file_object = open('collector.txt')
try:
    collector_ID = file_object.read()
    COL = collector_ID
    print COL
finally:
    file_object.close()
    
    
for i in range(1,5):
    print i    
    
dict_data['a'] = 'adfdfdsf'    
for key,value in dict_data.items():    
    print key,value
    
print datetime.datetime.now()  

d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print delta.days
print delta

def fun():
    print 'hello world!'

t = Timer(3.0,fun)
t.start() 

g = {}
while not g:
    print 'g dict is not empty'
    break

for i in range(1,5):
    print i
    g['layer_ID_'+str(i)] = {}
    g['layer_ID_'+str(i)]['light_status'] = '1' #got from collecor 
    g['layer_ID_'+str(i)]['ultraviolet_status'] = '0' #got from collecor 
    print 'layer_ID_'+str(i)
    
a_json = json.dumps(a)
a_dic =json.loads(a_json)
print a_json
a_json_ = json.dumps(a_dic)
a_dic_ =json.loads(a_json_)
print a_json_