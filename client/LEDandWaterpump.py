import RPi.GPIO as GPIO
import logging
import time

#shelf_num=input("Enter value from 1 to 4:")
#e=input("Enter value 0 or 1:")

def ini_LED_waterdump():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    GPIO.setup(4,GPIO.OUT)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setup(27,GPIO.OUT)
    '''
    GPIO.output(18,True)
    GPIO.output(23,True)    
    GPIO.output(21,True)    
    GPIO.output(25,True)    
    GPIO.output(4,True)   
    GPIO.output(17,True)    
    GPIO.output(22,True)    
    GPIO.output(27,True)    
    time.sleep(2)
    '''
    GPIO.output(18,False)
    GPIO.output(23,False)    
    GPIO.output(21,False)    
    GPIO.output(25,False)    
    GPIO.output(4,False)   
    GPIO.output(17,False)    
    GPIO.output(22,False)    
    GPIO.output(27,False)
    
def LED_ctr(shelf_num,e):
    
    if(shelf_num==1 and e==1):
        GPIO.output(18,True)
    elif(shelf_num==1 and e==0):
        GPIO.output(18,False)
        
    elif(shelf_num==2 and e==1):
        GPIO.output(23,True)
    elif(shelf_num==2 and e==0):
        GPIO.output(23,False)
        
    elif(shelf_num==3 and e==1):
        GPIO.output(21,True)
    elif(shelf_num==3 and e==0):
        GPIO.output(21,False)
    
    elif(shelf_num==4 and e==1):
        GPIO.output(25,True)
    elif(shelf_num==4 and e==0):
        GPIO.output(25,False)
        
    else:
        #print('No this shelf')
        logging.info('shelf is error!')

   # finally:
     #   print("Cleaning Up!")
      #  GPIO.cleanup()

#LED_ctr(shelf_num,e)


#shelf_num=input("Enter value from 1 to 4:")
#f=input("Enter value 0 or 1:")

def Water_pump(shelf_num,f):
    
    
    logging.info('shelf_num = %d,f= %d',shelf_num,f)
    #try:
    if(shelf_num==1 and f==1):
        GPIO.output(4,True)
    elif(shelf_num==1 and f==0):
        GPIO.output(4,False)
        
    elif(shelf_num==2 and f==1):
        GPIO.output(17,True)
    elif(shelf_num==2 and f==0):    
        GPIO.output(17,False)
            
    elif(shelf_num==3 and f==1):
        GPIO.output(22,True)
    elif(shelf_num==3 and f==0):
        GPIO.output(22,False)
    
    elif(shelf_num==4 and f==1):
        GPIO.output(27,True)
    elif(shelf_num==4 and f==0):
        GPIO.output(27,False)   
    
    else:
        #print('No this shelf')
        logging.info('shelf is error!')
            
    #finally:
        #logging.info('Cleaning Up!')
        #print("Cleaning Up!")
        #GPIO.cleanup()

#Water_pump(shelf_num,f)
