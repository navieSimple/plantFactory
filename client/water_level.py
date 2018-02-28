import RPi.GPIO as GPIO
import logging
#import time
'''
GPIO.setmode(GPIO.BCM)

shelf_1_waterlevel_low =12
shelf_2_waterlevel_low =16
shelf_3_waterlevel_low =20
shelf_4_waterlevel_low =26

shelf_1_waterlevel_high =5
shelf_2_waterlevel_high =6
shelf_3_waterlevel_high =13
shelf_4_waterlevel_high =19

GPIO.setup(shelf_1_waterlevel_low,GPIO.IN)  #shelf 1   detect low water_lev
GPIO.setup(shelf_2_waterlevel_low,GPIO.IN)  #shelf 2   detect low water_lev
GPIO.setup(shelf_3_waterlevel_low,GPIO.IN)  #shelf 3   detect low water_lev
GPIO.setup(shelf_4_waterlevel_low,GPIO.IN)  #shelf 4   detect low water_lev

GPIO.setup(shelf_1_waterlevel_high,GPIO.IN)   #shelf 1  detect high water_lev  
GPIO.setup(shelf_2_waterlevel_high,GPIO.IN)   #shelf 2  detect high water_lev
GPIO.setup(shelf_3_waterlevel_high,GPIO.IN)  #shelf 3  detect high water_lev
GPIO.setup(shelf_4_waterlevel_high,GPIO.IN)  #shelf 4  detect high water_lev

#GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(shelf_1_waterlevel_low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_2_waterlevel_low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_3_waterlevel_low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_4_waterlevel_low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_1_waterlevel_high, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_2_waterlevel_high, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_3_waterlevel_high, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shelf_4_waterlevel_high, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def water_level_low(shelf_num):
    if shelf_num == 1:
        ret = GPIO.input(shelf_1_waterlevel_low)
    elif shelf_num == 2:
        ret = GPIO.input(shelf_2_waterlevel_low)
    elif shelf_num == 3:
        ret = GPIO.input(shelf_3_waterlevel_low)
    elif shelf_num == 4:
        ret = GPIO.input(shelf_4_waterlevel_low)
    else:
        logging.error('the number of the shelf is error!')
    
    return ret
    
def water_level_high(shelf_num):
    if shelf_num == 1:
        ret = GPIO.input(shelf_1_waterlevel_high)
    elif shelf_num == 2:
        ret = GPIO.input(shelf_2_waterlevel_high)
    elif shelf_num == 3:
        ret = GPIO.input(shelf_3_waterlevel_high)
    elif shelf_num == 4:
        ret = GPIO.input(shelf_4_waterlevel_high)
    else:
        logging.error('the number of the shelf is error!')
    
    return ret    
'''
    
    
    
    
    
    
