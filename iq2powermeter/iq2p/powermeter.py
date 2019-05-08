#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import visa
import re
import time
import csv

class N1911A():
    def __init__(self, ip):
        self.ip = ip
        self.address = 'TCPIP0::%s::inst0::INSTR' % self.ip
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.resourceManager.close()

    def reset(self):
        self.instance.write('*RST')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        #return idn

    def read_data(self, channel,targetpower,result_name,delaytime):
        self.instance.write('*CLS')
        time.sleep(1)
        self.instance.write('FORM ASC')
        time.sleep(1)
        self.instance.write('SENS:FREQ %sMhz' % channel)
        time.sleep(1)
        self.instance.write('INIT:CONT ON')
        time.sleep(1)
        self.instance.write('TRIG:SOUR IMM')
        time.sleep(1)
        self.instance.write('INIT:CONT OFF')
        time.sleep(1)
        data = self.instance.query('READ:SCALar:POW:AC?', delay=delaytime)
        power = float(data)
        power = '{:.3f}'.format(power)
        #return power
        print('PowerMeter:', power, 'dBm')
        with open('.\\Result\\' + result_name, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([channel, targetpower, power])

if __name__ == '__main__':
    n1911a = N1911A('192.168.100.222')
    n1911a.open()
    n1911a.read_idn()
    n1911a.reset()
    n1911a.read_data(2412, -10, '222', 30)
    n1911a.close()
