# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:23
# @Author  : Ethan
# @FileName: cal_pathloss.py

import csv
import datetime
import time
import re
import visa

class IQxel():
    def __init__(self, ip):
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
        #return idn

    def init(self):
        self.instance.write('ROUT1;PORT:RES RF1,OFF')
        self.instance.write('ROUT1;PORT:RES RF2,OFF')
        #print('iq init...')


    def vsg(self,channel,targetpower,port,rout):
        self.instance.write('ROUT%s;PORT:RES RF%s,VSG%s' % (rout, port, rout))
        self.instance.write('CHAN1;WIFI')
        channels = float(channel) * 1000000
        self.instance.write('VSG%s;FREQ:cent %s' % (rout, channels))
        self.instance.write('VSA%s;SRAT 160000000' % rout)
        rlevel = targetpower
        self.instance.write('VSG%s;POW:lev %s' % (rout, rlevel))
        self.instance.write('VSG%s;WAVE:EXEC ON' % rout)
        self.instance.write('VSG%s;MOD:STAT OFF' % rout)
        self.instance.write('VSG%s;POW:STAT ON' % rout)
        #self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_OFDM-54.iqvsg"')
        print('Channel:', channel, 'VSG_Power:', rlevel, 'dBm', 'Waveform:', 'CW')

class N1911A():
    def __init__(self, ip):
        self.ip = ip
        #self.visaDLL = 'c:/windows/system32/visa32.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::inst0::INSTR' % self.ip
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)
        #print (self.address)
        #self.instance.write('*TST?')
        #print (self.instance)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def reset(self):
        self.instance.write('*RST')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        #return idn


    def read_data(self, channel,targetpower,result_name,delaytime):
        #self.instance.write('*RST')
        #time.sleep(1)
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
        data = self.instance.query('READ:SCAL:POW:AC?', delay=delaytime)
        power = float(data)
        power = '{:.3f}'.format(power)
        #return power
        print('Powermeter:', power, 'dBm')
        with open('./Result/' + result_name, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([channel, targetpower, power])


if __name__ == '__main__':
    print('**********************WELCOME***********************')
    dut_file = csv.reader(open('./config.csv'))
    for rows in dut_file:
        if rows[0] == 'IQ_IP':
            iq_ip = rows[1]
            print('IQ IP: ', iq_ip)
        elif rows[0] == 'IQ_ROUT':
            iq_rout = rows[1]
            print('IQ ROUT: ', iq_rout)
        elif rows[0] == 'IQ_PORT':
            iq_port = rows[1]
            print('IQ PORT: ', iq_port)
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

    #REPORT
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
    print('Result File:', result_name)

    #TEST FLOW
    for i in freq:
        iq.vsg(i, pw, iq_rout, iq_port)
        n1911a.read_data(i, pw, result_name, dt)
    iq.close()
    n1911a.close()
    print('***********************DONE************************')