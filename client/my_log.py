import logging
import global_list
from logging.handlers import RotatingFileHandler
def log_conf():
    '''
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=global_list.log_file,
                    filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(filename)s[line:%(lineno)d] %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    '''

    Rthandler = RotatingFileHandler(global_list.log_file, maxBytes=10*1024*1024,backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger('').setLevel(logging.INFO)
    logging.getLogger('').addHandler(Rthandler)