# -*- coding: utf-8 -*-
#!/usr/bin/env python
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
            #self.instance = None

    def reset(self):
        self.instance.write('*RST;*wai;*opc?')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        #return idn

    def vsg(self, channel, target_power, mw, rout, port):
        if mw == '1':
            mws = 'M'
        else:
            mws = ''
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mws, rout, port, rout))
        self.instance.write('CHAN1;WIFI')
        channels = float(channel) * 1000000
        self.instance.write('%sVSG%s;FREQ:cent %s' % (mws, rout, channels))
        self.instance.write('%sVSG%s;POW:lev %s' % (mws, rout, target_power))
        self.instance.write('%sVSG%s;WAVE:EXEC ON' % (mws, rout))
        self.instance.write('%sVSG%s;MOD:STAT OFF' % (mws, rout))
        self.instance.write('%sVSG%s;POW:STAT ON' % (mws, rout))
        #self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_OFDM-54.iqvsg"')
        print('Channel:', channel, 'VSG_Power:', target_power, 'dBm', 'Waveform:', 'CW')

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
            #self.instance = None

    def reset(self):
        self.instance.write('*RST')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        #return idn

    def read_data(self, channel, targetpower, result_name, avg_count, delaytime):
        #self.instance.write('*RST')
        #time.sleep(1)
        self.instance.write('*CLS')
        #time.sleep(1)
        self.instance.write('FORM ASC')
        #time.sleep(1)
        self.instance.write('SENS:FREQ %sMhz' % channel)
        #time.sleep(1)
        self.instance.write('INIT:CONT ON')
        #time.sleep(1)
        self.instance.write('TRIG:SOUR IMM')
        self.instance.write(':SENSe:AVERage:COUNt %d' % avg_count)
        #time.sleep(1)
        self.instance.write('INIT:CONT OFF')
        #time.sleep(1)
        data = self.instance.query('READ:SCALar:POW:AC?', delay=delaytime)
        power = float(data)
        power = '{:.3f}'.format(power)
        #return power
        print('PowerMeter:', power, 'dBm')
        with open('.\\Result\\' + result_name, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([channel, targetpower, power])

if __name__ == '__main__':
    print('**********************WELCOME***********************')
    iq_ip = mw = iq_rout = iq_port = pm_ip = pw = dt = freq = None
    dut_file = csv.reader(open('./config.csv'))
    for rows in dut_file:
        if rows[0] == 'IQ_IP':
            iq_ip = rows[1]
            print('IQ IP: ', iq_ip)
        elif rows[0] == 'IQ_MW':
            mw = rows[1]
            print('MW: ', mw)
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
            pw = re.sub(' ', '', pw)
            pw = pw.split(';')
            print('IQ VSG POWER: ', pw, 'dBm')
        elif rows[0] == 'delay_time':
            dt = float(rows[1])
            print('DelayTime: ', dt, 's')
        elif rows[0] == 'avg_count':
            avg = float(rows[1])
            print('AVG_COUNT: ', avg)
        elif rows[0] == 'Cal_Frequency':
            freq = rows[1]
            freq = re.sub(' ', '', freq)
            freq = freq.split(';')
            print('Cal_Frequency: ', freq, 'MHz')

    #INIT IQ
    iq = IQxel(iq_ip)
    iq.open()
    iq.read_idn()
    iq.reset()

    #INIT POWERMETER
    n1911a = N1911A(pm_ip)
    n1911a.open()
    n1911a.read_idn()#
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
    result_name = 'Path_loss' + '_' + iq_port + '_' + now_time + '.csv'
    with open('.\\Result\\' + result_name, 'w', newline='') as file:
        writer_result = csv.writer(file)
        writer_result.writerow(['IQ_ROUT', iq_rout, 'IQ_PORT', iq_port])
        writer_result.writerow(['FREQ', 'IQ_VSG_POWER', 'POWER_METER_RESULT'])
    print('Result File:', result_name)

    #TEST FLOW
    for j in pw:
        for i in freq:
            iq.vsg(i, j, mw, iq_rout, iq_port)
            n1911a.read_data(i, j, result_name, avg, dt)
    iq.close()
    n1911a.close()
    print('***********************DONE************************')