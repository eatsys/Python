# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx_test.py

from iq import IQxel
from powermeter import N1911A
import csv
import datetime
import time
import re
from openpyxl import load_workbook
import os


try:
    print('############ WELCOME #############')
    dut_file = csv.reader(open('./config.csv'))
    for rows in dut_file:
        if rows[0] == 'IQ_IP':
            iq_ip = rows[1]
            print('IQ IP: ', iq_ip)
        elif rows[0] == 'PowerMeter_IP':
            pm_ip = rows[1]
            print('PowerMeter IP: ', pm_ip)
        elif rows[0] == 'IQ_VSG_POWER':
            pw = rows[1]
            print('IQ VSG POWER: ', pw, 'dBm')
        elif rows[0] == 'delaytime':
            dt = float(rows[1])
            print('DelayTime: ', dt, 's')
        elif rows[0] == 'Cal_Frequency':
            freq = rows[1]
            freq = freq.split(';')
            #freq = freq.append()
            print('Cal_Frequency: ', freq)

    #INIT IQ
    iq = IQxel(iq_ip)
    iq.open()
    iq.read_idn()
    iq.init()

    #INIT POWERMETER
    n1911a = N1911A(pm_ip)
    n1911a.open()
    n1911a.read_idn()
    n1911a.reset()

    #INIT SPEC

    now_time = datetime.datetime.now()
    now_time = str(now_time)
    now_time = now_time.split()
    day_time = re.sub('-', '', now_time[0])
    now_time = now_time[1].split('.')
    now_time = re.sub(':', '', now_time[0])
    now_time = day_time + now_time
    #print(now_time)
    result_name = 'pathloss' + '_' + now_time + '.csv'
    with open('./Result/' + result_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['FREQ', 'IQ_VSG_POWER', 'POWER_METER_RESULT'])
    print(result_name)

    #TEST FLOW
    for i in freq:
        iq.vsg(i, pw, 'cw')
        n1911a.read_data(i, pw, result_name, dt)
    #print('*************************************************************')

    iq.close()
    n1911a.close()

finally:
    time.sleep(1)