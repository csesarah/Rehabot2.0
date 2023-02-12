'''
__author       = "Chen Si-En, Sarah"
__copyright    = "Copyright 2021, Chen Si-En, Sarah"

__description  = "Functions for reading and recording Arduino IMU data"
__version      = "1.1.0"
__status       = "Production"
__dependencies = "serial, sys, global_params.py"
'''

from serial.threaded import LineReader
import global_params
import sys
from time import time

class SerialReaderProtocol(LineReader):
    ''' THREADED SERIAL READER
            
    '''

    def connection_made(self, transport):
        print("Connected ...")

    def handle_line(self, data):
        updateData(data)

def updateData(data):
    ''' PRINT DATA TO CONSOLE WHEN DATA IS AVAILABLE
            
    '''

    print(str(time())+','+data)

def recordStream():
    ''' RECORD PRINTED DATA TO CSV FILE
            
    '''

    orig_stdout = sys.stdout
    f = open('datafile.csv', 'w')
    sys.stdout = f
    
    if global_params.stop_recordStream:
        sys.stdout = orig_stdout
        f.close()
