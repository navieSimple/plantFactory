#coding=utf-8
#import sys
import MySQLdb
import time
import global_list
import logging
#import json
#import pymysql
import cv2
import numpy
import base64
 
def mysql_conn():
    
    global_list.conn= MySQLdb.connect(
        host='localhost',
        #port = 19964,
        user='root',
        passwd='cqgdxxyjy@123',
        db ='plant',
        )
    global_list.conn.ping(True)
    global_list.cur = global_list.conn.cursor()   
    #logging.info('Recieve data in the thread_trade: %s',global_list.trade_dict_data)
    logging.info('mysql connection success!!!')
    #print 'mysql connection success!!!'   

# get the number of the layer
# ‘fun_ID’:’010’   
def get_layernum(dic):
    collector_ID = dic['collector_ID']
    sql_select = "select layer_numbers from plant_shelf where collector_id = "
    global_list.cur.execute(sql_select+collector_ID)
    numrow = int(global_list.cur.rowcount)
    dic_1 ={}
    if numrow == 1:
        row = global_list.cur.fetchone()
        dic_1 = {'fun_ID':'010','collector_ID':collector_ID,'layer_num':str(row[0])}
        logging.info(dic_1)
    else:
       logging.error('collector ID is %s, shelf number is error',collector_ID)
       
    return dic_1
    
# update the scheme about on or off light time 
#‘fun_ID’:’011’
def update_lighttime_scheme(dic):
    dic_1 ={}
    
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        
        sql_select = 'select light_scheme_id from plant_layers where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        global_list.cur.execute(sql_select)
        numrow = int(global_list.cur.rowcount)       
        
        if numrow == 1:
            row = global_list.cur.fetchone()
            light_scheme_id = str(row[0])
        
            sql_update = 'update plant_layers set light_automanual_mode = '+dic['light_mode']\
                +','+'light_onoff_state = '+dic['light_on_off_state']\
                +' where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
            logging.info(sql_update)
            try:
                global_list.cur.execute(sql_update)
                global_list.conn.commit()
                logging.info('update database success!!! FunctionID=011')
            except:
                global_list.conn.rollback()
                logging.error('update database failed... FunctionID=011')
        
            sql_select = 'select light_open_time,light_close_time from light_control_scheme where light_scheme_id = '+light_scheme_id
            global_list.cur.execute(sql_select)
            numrow = int(global_list.cur.rowcount)
            
            if numrow == 1:
                row = global_list.cur.fetchone()
                dic_1 = {'fun_ID':'011','collector_ID':dic['collector_ID'],'layer_ID':dic['layer_ID'],'start_time':row[0],'end_time':row[1]}
            else:
                logging.error('light scheme no exist') 

        else:
            logging.error('light scheme ID is error')        
        
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
       
    return dic_1

'''
    sql_update = 'update v_function_011 set light_open_time = '+dic['start_time']\
            +','+'light_close_time = '+dic['end_time']\
            +' where collector_id = '+dic['collector_ID']\
            +' and '+'layer_num = '+dic['layer_ID']
    logging.info(sql_update)
    try:
        global_list.cur.execute(sql_update)
        global_list.conn.commit()
        logging.info('update database success1!!! FunctionID=011')
    except:
        global_list.conn.rollback()
        logging.error('update database failed1... FunctionID=011')
   
    sql_update = 'update v_function_011 set light_automanual_mode = '+dic['light_mode']\
            +','+'light_onoff_state = '+dic['light_on_off_state']\
            +' where collector_id = '+dic['collector_ID']\
            +' and '+'layer_num = '+dic['layer_ID']
    logging.info(sql_update)
    try:
        global_list.cur.execute(sql_update)
        global_list.conn.commit()
        logging.info('update database success!!! FunctionID=011')
        dic_1 = {'fun_ID':'011','layer_ID':dic['layer_ID']}
    except:
        global_list.conn.rollback()
        logging.error('update database failed... FunctionID=011')
        
    return dic_1
'''
    
#update the scheme about on or off water cycle in the growth zone
#‘fun_ID’:’012’
def update_watercycle_scheme_growthzone(dic):
    dic_1 ={}
    sql_select = 'select shelf_id,plant_shelf_water_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        plant_shelf_water_id = str(row[1])
        
        sql_select = 'select plant_layer_water_id from plant_layers where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        global_list.cur.execute(sql_select)
        numrow = int(global_list.cur.rowcount)       
        
        if numrow == 1:
            row = global_list.cur.fetchone()
            plant_layer_water_id = str(row[0])
        
            sql_update = 'update plant_layers set water_automanual_mode = '+dic['cycle_mode']\
                +','+'water_onoff_state = '+dic['cycle_state']\
                +' where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
            logging.info(sql_update)
            try:
                global_list.cur.execute(sql_update)
                global_list.conn.commit()
                logging.info('update database success!!! FunctionID=012')
            except:
                global_list.conn.rollback()
                logging.error('update database failed... FunctionID=012')
        
            sql_select = 'select plant_shelf_water_rest_time from plantshelf_water_control_scheme where plant_shelf_water_id = '+plant_shelf_water_id
            global_list.cur.execute(sql_select)
            numrow = int(global_list.cur.rowcount)
            
            if numrow == 1:
                row = global_list.cur.fetchone()
                plant_shelf_water_rest_time = str(row[0])
                
                sql_select = 'select plant_layer_water_run_time from plant_water_cycle_control_scheme where plant_layer_water_id = '+plant_layer_water_id
                global_list.cur.execute(sql_select)
                numrow = int(global_list.cur.rowcount)
                
                if numrow == 1:
                    row = global_list.cur.fetchone()
                
                    dic_1 = {'fun_ID':'012','collector_ID':dic['collector_ID'],'layer_ID':dic['layer_ID'],'cycle_time':row[0],'waiting_time':plant_shelf_water_rest_time}
                else:
                    logging.error('plant_water_cycle_control_scheme no exist') 
            else:
                logging.error('plantshelf_water_rest_scheme no exist') 

        else:
            logging.error('water scheme ID is error')        
        
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
       
    return dic_1
    
#update the scheme about on or off water cycle in the nursery zone
#‘fun_ID’:’013’
def update_watercycle_scheme_nurseryzone(dic):
    dic_1 ={}
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        
        sql_select = 'select seed_water_id from plant_layers where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        global_list.cur.execute(sql_select)
        numrow = int(global_list.cur.rowcount)       
        
        if numrow == 1:
            row = global_list.cur.fetchone()
            seed_water_id = str(row[0])
        
            sql_update = 'update plant_layers set water_automanual_mode = '+dic['cycle_mode']\
                +','+'water_onoff_state = '+dic['cycle_state']\
                +' where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
            logging.info(sql_update)
            try:
                global_list.cur.execute(sql_update)
                global_list.conn.commit()
                logging.info('update database success!!! FunctionID=013')
            except:
                global_list.conn.rollback()
                logging.error('update database failed... FunctionID=013')
        
            sql_select = 'select seed_water_timeout,seed_water_min,seed_water_max from seed_water_cycle_control_scheme where seed_water_id = '+seed_water_id
            global_list.cur.execute(sql_select)
            numrow = int(global_list.cur.rowcount)
            
            if numrow == 1:
                row = global_list.cur.fetchone()
                dic_1 = {'fun_ID':'013','collector_ID':dic['collector_ID'],'layer_ID':dic['layer_ID'],'timeout':row[0],'humi_min':row[1],'humi_max':row[2]}
            else:
                logging.error('water scheme no exist') 

        else:
            logging.error('water scheme ID is error')        
        
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
       
    return dic_1

# environment parameters of the zone
#‘fun_ID’:’02’
def zone_environment_parameters(dic):
    dic_1 = {'fun_ID': '02'}
    sql_select = 'select subarea_id from areas where area_collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        subarea_id = str(row[0])

        try:
            sql_update = 'update areas_environment_info set air_humidity = '+dic['zone_humi']\
                    +','+'air_temperature = '+dic['zone_temp']\
                    +','+'co2 = '+dic['co2']\
                    +' where subarea_id = '+subarea_id
            logging.info(sql_update)
            global_list.cur.execute(sql_update)
            sql_insert = 'insert into area_enviroment_history_information(subarea_id,co2,air_temperature,air_humidity) values('\
                +subarea_id+','+dic['co2']\
                +','+dic['zone_temp']\
                +','+dic['zone_humi']+')'
            logging.info(sql_insert)
            global_list.cur.execute(sql_insert)
            global_list.conn.commit()
        except:
            global_list.conn.rollback()
            logging.error('update or insert current environment info failed... FunctionID=02')
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
       
    return dic_1

# shelf parameters
#‘fun_ID’:’10’
def shelf_parameters(dic):
    dic_1 = {'fun_ID': '10'}
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        try:
            sql_update = 'update shelf_environment_info set water_level = '+dic['water_level']\
                    +','+'ph_value = '+dic['PH']\
                    +','+'ec_value = '+dic['EC']\
                    +','+'water_temperature = '+dic['water_temp']\
                    +' where shelf_id = '+shelf_id
            logging.info(sql_update)
            global_list.cur.execute(sql_update)
        
            sql_insert = 'insert into shelf_environment_history_information(shelf_id,water_temperature,ph_value,ec_value,water_level) values('\
                    +shelf_id+','+dic['water_temp']\
                    +','+dic['PH']\
                    +','+dic['EC']\
                    +','+dic['water_level']+')'
            logging.info(sql_insert)
            global_list.cur.execute(sql_insert)
            global_list.conn.commit()
        except:
            global_list.conn.rollback()
            logging.error('update or insert shelf environment info failed... FunctionID=10')
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
    
    return dic_1

# layer parameters
#‘fun_ID’:’11’
def layer_parameters(dic):
    dic_1 = {'fun_ID': '11'}
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
    
        sql_select = 'select layer_id from plant_layers where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        global_list.cur.execute(sql_select)
        numrow = int(global_list.cur.rowcount)
    
        if numrow == 1:
            row = global_list.cur.fetchone()
            layer_id = str(row[0])
            try:
                sql_update = 'update layer_environment_info set soil_humidity = '+dic['ave_humidity']\
                        +','+'light_value = '+dic['illumination']\
                        +' where shelf_id = '+shelf_id\
                        +' and '+'layer_id = '+layer_id
                logging.info(sql_update)
                global_list.cur.execute(sql_update)
                
                sql_insert = 'insert into layer_environment_history_information(layer_id,soil_humidity,light_value) values('\
                    +layer_id+','+dic['ave_humidity']\
                    +','+dic['illumination']+')'
                logging.info(sql_insert)
                global_list.cur.execute(sql_insert)
                global_list.conn.commit()
            except:
                global_list.conn.rollback()
                logging.error('update or insert layer environment info failed... FunctionID=11')
        else:
            logging.error('shelf ID= %s is error',shelf_id)
    
    else:
       logging.error('collector ID= %s is error',dic['collector_ID'])
       
    return dic_1

# process the light on or off
#‘fun_ID’:’03’ 
def light_on_off_process(dic):
    '''
    sql_update = 'update v_function_03 set light_onoff_state = '+dic['light_on_off']\
            +' where collector_id = '+dic['collector_ID']\
            +' and '+'layer_num = '+dic['layer_ID']
    '''
    sql_select = 'select shelf_id from plant_shelf where collector_id = ' + dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        sql_update = 'update plant_layers set light_onoff_state = ' + str(dic['light_on_off']) \
                     + ' where shelf_id = ' +  shelf_id\
                     + ' and ' + 'layer_num = ' + str(dic['layer_ID'])
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=03')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=03')
    else:
        logging.error("collector_ID error!")
        return

#update light state when it is time out
#‘fun_ID’:’13’
def update_light_state(dic):
    dic_1 = {'fun_ID': '13', 'layer_ID': dic['layer_ID']}
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)

    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
        sql_update = 'update plant_layers set light_onoff_state = '+dic['light_on_off_state']\
                +' where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=13')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=13')
    else:
        logging.error("collector_ID error!")
    return dic_1

# the light of the layer start or quit auto mode
#‘fun_ID’:’12’
def light_mode(dic):
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+str(dic['collector_ID'])
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
    
        sql_update = 'update plant_layers set light_automanual_mode = '+ str(dic['light_mode'])\
                +' where shelf_id = '+ shelf_id\
                +' and '+'layer_num = '+ str(dic['layer_ID'])
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=12')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=12')
    else:
        logging.error("collector_ID error!")

# the water cycle of certain layer start or quit auto mode in the growth zone
#‘fun_ID’:’06’
def layer_watercyle_mode_growthzone(dic):
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+ str(dic['collector_ID'])
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])
    
        sql_update = 'update plant_layers set water_automanual_mode = '+ str(dic['cycle_mode'])\
                +' where shelf_id = '+ shelf_id\
                +' and '+'layer_num = '+ str(dic['layer_ID'])
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=06')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=06')
    else:
        logging.error("collector_ID error!")

# the water cycle of certain layer start or quit auto mode in the nursery zone
#‘fun_ID’:’08’ 
def layer_watercyle_mode_nurseryzone(dic):
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+ str(dic['collector_ID'])
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])    
    
        sql_update = 'update plant_layers set water_automanual_mode = '+ str(dic['cycle_mode'])\
                +' where shelf_id = '+ shelf_id\
                +' and '+'layer_num = '+ str(dic['layer_ID'])
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=08')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=08')
    else:
        logging.error("collector_ID error!")

# the water cycle of certain layer on or off by manual mode in the nursery zone
#‘fun_ID’:’09’
def layer_watercyle_onoff_manual_nurseryzone(dic):
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+ str(dic['collector_ID'])
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0])  
    
        sql_update = 'update plant_layers set water_onoff_state = '+ str(dic['cycle_state'])\
                +','+'water_automanual_mode = '+ str(dic['cycle_mode'])\
                +' where shelf_id = '+ shelf_id\
                +' and '+'layer_num = '+ str(dic['layer_ID'])
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=09')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=09')
    else:
        logging.error("collector_ID error!")

#update water cycle state when it is doing
#‘fun_ID’:’14’
def update_watercycle_state(dic):
    dic_1 = {'fun_ID': '14', 'layer_ID': dic['layer_ID']}
    sql_select = 'select shelf_id from plant_shelf where collector_id = '+dic['collector_ID']
    global_list.cur.execute(sql_select)
    numrow = int(global_list.cur.rowcount)
    
    if numrow == 1:
        row = global_list.cur.fetchone()
        shelf_id = str(row[0]) 

        sql_update = 'update plant_layers set water_onoff_state = '+dic['cycle_state']\
                +' where shelf_id = '+shelf_id\
                +' and '+'layer_num = '+dic['layer_ID']
        logging.info(sql_update)
        try:
            global_list.cur.execute(sql_update)
            global_list.conn.commit()
            logging.info('update database success!!! FunctionID=14')
        except:
            global_list.conn.rollback()
            logging.error('update database failed... FunctionID=14')
    else:
        logging.error("collector_ID error!")
    return dic_1

def process_position_camera_capture(dic):
    try:
        #data = numpy.fromstring(dic['image'], dtype='uint8')
        data = base64.b64decode(dic['image'])
        jpg_np = numpy.frombuffer(data, dtype='uint8')
        dec_mage = cv2.imdecode(jpg_np,1)
        #size = dec_mage.shape
        #rows = size[0]
        #cols = size[1]
        #logging.info("image: row[%d] cols[%d]", rows, cols)
        #M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1)
        #dst = cv2.warpAffine(dec_mage, M, (cols, rows))
        cur_time = time.localtime()
        date_time = str(cur_time[0]) + '-' + str(cur_time[1]) + \
                         '-' + str(cur_time[2]) + ' ' + str(cur_time[3]) + '-' + str(cur_time[4])
        logging.info("data_time:%s", date_time)
        '''
        image_name = global_list.g_image_dir + dic['collector_ID'] + '_' +\
                    'position' + dic['position_ID'] + '_' + str(cur_time[0]) + '.'+str(cur_time[1])+\
                     '.'+str(cur_time[2])+'_'+str(cur_time[3])+'.'+str(cur_time[4]) + '.jpg'
        cv2.imwrite(image_name, dec_mage)
        
        
        TODO: 
           add. 更新数据库对应的图像路径
           modify: 图像储存路径global_list.g_image_dir
        '''
        sql_select = 'select shelf_id from plant_shelf where collector_id = ' + dic['collector_ID']
        global_list.cur.execute(sql_select)
        numrow = int(global_list.cur.rowcount)
        if numrow ==1:
            row = global_list.cur.fetchone()
            shelf_id = str(row[0])
            image_name = 'shelf'+ shelf_id + '_' + \
                         'position' + dic['position_ID'] + '_' + date_time + '.jpg'
            image_dir = global_list.g_image_dir + image_name
            image_database_dir = global_list.g_database_img_dir + image_name
            cv2.imwrite(image_dir, dec_mage)
            #sql_insert = 'insert into figures_history_of_shelf (shelf_id, figure_path, positon, credate)\
            #                  VALUES (%s,%s,%s,%s)'
            #insert_param = [shelf_id, image_name, dic['position_ID'], date_time]
            #global_list.cur.execute(sql_insert, insert_param)
            sql_insert = "insert into figures_history_of_shelf (shelf_id, figure_path, positon, credate) \
                         VALUES (%d,'%s','%s','%s')" %(int(shelf_id), image_database_dir, dic['position_ID'], date_time)
            global_list.cur.execute(sql_insert)
            sql_select1 = 'select * from figure_current_of_shelf where shelf_id = ' + shelf_id + ' and  positon = '\
                                + dic['position_ID']
            global_list.cur.execute(sql_select1)
            numrow1 = int(global_list.cur.rowcount)
            if numrow1 == 0:
                logging.info("figure_current_of_shelf has no values. insert...")
                #sql_insert =  'insert into figure_current_of_shelf (shelf_id, figure_path, positon, credate)\
                #             VALUES (%s,%s,%s,%s)'
                #global_list.cur.execute(sql_insert, insert_param)
                sql_insert = "insert into figure_current_of_shelf (shelf_id, figure_path, positon, credate) \
                             VALUES (%d,'%s','%s','%s')" %(int(shelf_id), image_database_dir, dic['position_ID'], date_time)
                global_list.cur.execute(sql_insert)
            else:
                logging.info("figure_current_of_shelf has values. update...")
                #sql_update = 'update figure_current_of_shelf set figure_path = ' + image_name + ' , credate = '\
                #            + date_time + ' where shelf_id =' + shelf_id + ' and  positon = ' + dic['position_ID']
                sql_update = "update figure_current_of_shelf set figure_path = '%s', " \
                                    "credate = '%s' where shelf_id = %d and positon = '%s'" \
                                    %(image_database_dir, date_time, int(shelf_id), dic['position_ID'])
                global_list.cur.execute(sql_update)
            global_list.conn.commit()
        else:
            logging.error("query shelf id failed!")
    except Exception as e:
        #print (e)
        logging.error('process_position_camera_capture failed... FunctionID=15')
        global_list.conn.rollback()

