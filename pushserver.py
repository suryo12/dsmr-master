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

    #baca serial dari rs485
    rs485 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    rs485.serial.baudrate = 2400
    rs485.serial.bytesize = 8
    rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
    rs485.serial.stopbits = 1
    rs485.serial.timeout = 1
    rs485.debug = False
    rs485.mode = minimalmodbus.MODE_RTU
    #print rs485

    #realtime dari raspberry
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S+02')

    #buat variabel bacaan dari rs485
    Volts = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
    Current = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
    Active_Power = rs485.read_float(12, functioncode=4, numberOfRegisters=2)/1000
    Apparent_Power = rs485.read_float(18, functioncode=4, numberOfRegisters=2)
    Reactive_Power = rs485.read_float(24, functioncode=4, numberOfRegisters=2)
    Power_Factor = rs485.read_float(30, functioncode=4, numberOfRegisters=2)
    Phase_Angle = rs485.read_float(36, functioncode=4, numberOfRegisters=2)
    Frequency = rs485.read_float(70, functioncode=4, numberOfRegisters=2)
    Import_Active_Energy = rs485.read_float(72, functioncode=4, numberOfRegisters=2) 
    Export_Active_Energy = rs485.read_float(74, functioncode=4, numberOfRegisters=2)
    Import_Reactive_Energy = rs485.read_float(76, functioncode=4, numberOfRegisters=2)
    Export_Reactive_Energy = rs485.read_float(78, functioncode=4, numberOfRegisters=2)
    Total_Active_Energy = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
    Total_Reactive_Energy = rs485.read_float(344, functioncode=4, numberOfRegisters=2)

    #konversi jumlah digit
    daya_sekarang=float("{0:.3f}".format(Active_Power))
    energi_masuk_total=float("{0:.5f}".format(Total_Active_Energy))
    energi_keluar=float("{0:.5f}".format(Export_Active_Energy))
    
    print ("Daya saat ini: ", daya_sekarang, "Watt") 
    #print "Energi Total Hari Ini: ", energi_masuk_total, "KWH"
    print (st)
    
    response = requests.post(
    'http://localhost:8000/api/v2/datalogger/dsmrreading',
    headers={'X-AUTHKEY': '2F31RWYH2LXPMQ2QXNV50HV2I1NBCVJU6PNDAUG7M47R4HO93N7P4TC8T5Q6FU7J'},
    data={
        'electricity_currently_delivered': daya_sekarang,
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
