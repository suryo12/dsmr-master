#!/usr/bin/env python3

import minimalmodbus #install minimalmodbus library http://minimalmodbus.readthedocs.io/en/master/installation.html
import requests
import json
#import MySQLdb
import serial
import time
import datetime
import sched

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 

    ser = serial.Serial('/dev/ttyUSB1', baudrate = 2400, timeout=1)

    while 1:
    
        arduinoData = ser.readline().decode('ascii')
        print arduinoData

        #realtime dari raspberry
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S+02')

        response = requests.post(
        'http://localhost:8000/api/v2/datalogger/dsmrreading',
        headers={'X-AUTHKEY': '2F31RWYH2LXPMQ2QXNV50HV2I1NBCVJU6PNDAUG7M47R4HO93N7P4TC8T5Q6FU7J'},
        data={
        'electricity_currently_delivered': arduinoData,
        'electricity_currently_returned': 0,
        'electricity_delivered_1': 0,
        'electricity_delivered_2': 0,
        'electricity_returned_1': 0,
        'electricity_returned_2': 0,
        'timestamp': st,
             }
            )
    
    s.enter(10, 1, do_something, (sc,))

s.enter(10, 1, do_something, (s,))
s.run()

if response.status_code != 201:
    print('Error: {}'.format(response.text))
else:
    print('Created: {}'.format(json.loads(response.text)))
