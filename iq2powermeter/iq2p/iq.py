#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author:Ethan


from __future__ import division
import visa
import pandas as pd
import time
from colorama import Fore, Back, Style
import csv
from openpyxl import load_workbook
import datetime
import re

# rm = visa.ResourceManager()
# #print (rm)
# inst = rm.open_resource('TCPIP0::192.168.100.254::hislip0::INSTR')
# print (inst)
# Q = inst.query('*IDN?')
# print (Q)
# inst.write('MROUT1;PORT:RES RF1,OFF')

log_switch = 0
sleep_time = 0.2

class IQxel():
    def __init__(self, ip, visaDLL=None, *args):
        self.ip = ip
        #self.visaDLL = 'C:\windows\system32\visa64.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::hislip0::INSTR' % self.ip
        #self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)
        #print(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def __format__(self, format_spec):
        self.format_spec = format_spec
        format_spec = float(format_spec)
        format_spec = '{:.3f}'.format(format_spec)
        return format_spec

    def reset(self):
        self.instance.write('*RST')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        return idn

    def init(self):
        self.instance.write('ROUT1;PORT:RES RF1,OFF')
        self.instance.write('ROUT1;PORT:RES RF2,OFF')
        #print('iq init...')


    def vsg(self,channel,targetpower):
        self.instance.write('ROUT1;PORT:RES RF1,VSG1')
        self.instance.write('CHAN1;WIFI')
        channels = channel * 1000000
        self.instance.write('VSA1;FREQ:cent %s' % channels)
        self.instance.write('VSA1;SRAT 160000000')
        # self.instance.write('VSA1 ;RLEVel:AUTO')
        rlevel = targetpower
        # print(rlevel)
        time.sleep(sleep_time)
        self.instance.write('VSG1;POW:lev %s' % rlevel)
        self.instance.write('VSA1;RFC:USE "1",RF1')
        self.instance.write('VSA1;RFC:STAT  ON,RF1')
        self.instance.write('VSG1;WAVE:EXEC ON')
        self.instance.write('VSG1;MOD:STAT OFF')
        self.instance.write('VSG1;POW:STAT ON')
        #self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_OFDM-54.iqvsg"')
        print('Channel:',channel,'VSG_Power:',rlevel,'dBm','Waveform:','CW')


if __name__ == '__main__':
    iq = IQxel('192.168.100.254')
    iq.open()
    iq.read_idn()
    iq.init()
    iq.vsg(5150,-10)
    iq.close()