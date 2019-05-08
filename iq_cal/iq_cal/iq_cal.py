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

class instance():
    def __init__(self, ip):
        self.ip = ip
        #self.visaDLL = 'C:\windows\system32\visa64.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::hislip0::INSTR' % self.ip
        #self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)
        #print(self.address)
        #self.instance.timeout = 5000
        #self.instance.read_termination = '\n'

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.resourceManager.close()
            #self.instance = None

    def reset(self):
        self.instance.write('*RST;*wai;*opc?')

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        print(idn)
        #return idn

    def vsg(self, channel, target_power):
        if mw == '1':
            mws = 'M'
        else:
            mws = ''
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mws, vsg_rout, vsg_port, vsg_rout))
        self.instance.write('CHAN1;WIFI')
        channels = float(channel) * 1000000
        self.instance.write('%sVSG%s;FREQ:cent %s' % (mws, vsg_rout, channels))
        self.instance.write('%sVSG%s;POW:lev %s' % (mws, vsg_rout, target_power))
        self.instance.write('%sVSG%s;SRAT 160000000' % (mws, vsg_rout))
        self.instance.write('%sVSG%s; WAVE:LOAD "/user/WiFi_QUAR-6.iqvsg"' % (mws, vsg_rout))
        self.instance.write('%sVSG%s;WAVE:EXEC ON' % (mws, vsg_rout))
        self.instance.write('%sVSG%s;MOD:STAT ON' % (mws, vsg_rout))
        self.instance.write('%sVSG%s;POW:STAT ON' % (mws, vsg_rout))
        print('Channel:', channel, 'VSG_Power:', target_power, 'dBm', 'Waveform:', 'WiFi_QUAR-6')

    def read_data(self, channel):
        if mw == '1':
            mws = 'M'
        else:
            mws = ''
        #print(channel, target_power, mw, vsa_rout, vsa_port, vsg_port, result_name)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSA%s' % (mws, vsa_rout, vsa_port, vsa_rout))
        #print('%sROUT%s;PORT:RES RF%s,VSA%s' % (mws, vsa_rout, vsa_port, vsa_rout))
        channels = float(channel) * 1000000
        self.instance.write('%sVSA%s;FREQ:cent %s' % (mws, vsa_rout, channels))
        #print('%sVSA%s;FREQ:cent %s' % (mws, vsa_rout, channels))
        self.instance.write('%sVSA%s;SRAT 160000000' % (mws, vsa_rout))
        #print('%sVSA%s;SRAT 160000000' % (mws, vsa_rout))
        self.instance.write('%sVSA%s ;RLEVel:AUTO' % (mws, vsa_rout))
        #print('%sVSA%s;RLEV:AUTO;*wai;*opc?' % (mws, vsa_rout))#
        #rlevel = float(target_power) + 15
        #print(rlevel)
        time.sleep(1)
        #self.instance.write('WIFI;CLE:POW;*wai;*opc?')
        self.instance.write('%sVSA%s;CAPT:TIME 0.02' % (mws, vsa_rout))
        #print('%sVSA%s;CAPT:TIME 0.02' % (mws, vsa_rout))
        #self.instance.write('%sVSA%s;RLEVel %s;*wai;*opc?' % (mws, vsa_rout, rlevel))
        #time.sleep(2)
        self.instance.write('CHAN1')
        self.instance.write('%sVSA%s ;init' % (mws, vsa_rout))
        #print('%sVSA%s ;init' % (mws, vsa_rout))
        self.instance.write('WIFI')
        self.instance.write('calc:pow 0, 10')
        #self.instance.write('calc:txq 0, 10')
        #self.instance.write('calc:ccdf 0, 10')
        #self.instance.write('calc:ramp 0, 10')
        #self.instance.write('calc:spec 0, 10')
        # print(rec)
        time.sleep(1)
        rdata = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
        #print('2', rdata)
        ##datas = eval(data)
        ##print(datas)
        #time.sleep(1)
        #rdata = rdata.split(',')
        #rdata = rdata[0]
        #power = float(rdata)
        #power = '{:.3f}'.format(power)
        #print('Power:', power, 'dBm')
        #with open('.\\Result\\' + result_name, 'a+', newline='') as f:
        #    writer = csv.writer(f)
        #    writer.writerow([vsg_port, channel, target_power, power])


    def get_data(self, channel, target_power):
        #self.instance.write('ROUT1;PORT:RES RF1,VSA1')
        #self.instance.write('VSA1;FREQ:cent 2412000000')
        #self.instance.write('VSA1;SRAT 160000000')
        ##self.instance.write('WIFI;CLE:POW;*wai;*opc?')
        #self.instance.write('VSA1;CAPT:TIME 0.02')
        #self.instance.write('CHAN1')
        #self.instance.write('VSA1 ;init')
        #self.instance.write('WIFI')
        #self.instance.write('calc:pow 0, 10')
        retval = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
        #print(retval)
        retval = retval.split(',')
        retval = retval[1]
        power = float(retval)
        power = '{:.3f}'.format(power)
        print('VSA_PORT:', vsa_port, 'Power:', power, 'dBm')
        with open('.\\Result\\' + result_name, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([vsg_port, channel, target_power, vsa_port, power])

if __name__ == '__main__':
    print('************************WELCOME*************************')
    iq_ip = mw = iq_rout = iq_port = pm_ip = pw = dt = freq = None
    dut_file = csv.reader(open('./config.csv'))
    for rows in dut_file:
        if rows[0] == 'IQ_IP':
            iq_ip = rows[1]
            print('IQ IP: ', iq_ip)
        elif rows[0] == 'IQ_MW':
            mw = rows[1]
            print('MW: ', mw)
        elif rows[0] == 'IQ_ROUT_VSG':
            vsg_rout = rows[1]
            print('IQ ROUT VSG: ', vsg_rout)
        elif rows[0] == 'IQ_PORT_VSG':
            vsg_port = rows[1]
            print('IQ PORT VSG: ', vsg_port)
        elif rows[0] == 'IQ_ROUT_VSA':
            vsa_rout = rows[1]
            print('IQ ROUT VSA: ', vsa_rout)
        elif rows[0] == 'IQ_PORT_VSA':
            vsa_port = rows[1]
            print('IQ PORT VSA: ', vsa_port)
        elif rows[0] == 'IQ_VSG_POWER':
            pw = rows[1]
            pw = re.sub(' ', '', pw)
            pw = pw.split(';')
            print('IQ VSG POWER: ', pw, 'dBm')
        elif rows[0] == 'Cal_Frequency':
            freq = rows[1]
            freq = re.sub(' ', '', freq)
            freq = freq.split(';')
            print('Cal_Frequency: ', freq, 'MHz')

    #INIT IQ
    iq = instance(iq_ip)
    iq.open()
    iq.read_idn()
    iq.reset()

    #REPORT
    now_time = datetime.datetime.now()
    now_time = str(now_time)
    now_time = now_time.split()
    day_time = re.sub('-', '', now_time[0])
    now_time = now_time[1].split('.')
    now_time = re.sub(':', '', now_time[0])
    now_time = day_time + now_time
    #print(now_time)
    result_name = 'Pathloss' + '_' + 'VSA-PORT' + vsa_port + '_' + now_time + '.csv'
    with open('.\\Result\\' + result_name, 'w', newline='') as file:
        writer_result = csv.writer(file)
        writer_result.writerow(['IQ_VSG_PORT', 'FREQUENCY', 'IQ_VSG_TARGET_POWER', 'IQ_VSA_PORT', 'MEASURE_POWER'])
    print('Result File:', result_name)

    #TEST FLOW
    for j in pw:#
        for i in freq:
            #print(j,i,mw,vsg_rout,vsg_port,vsa_rout,vsa_port,result_name)
            iq.vsg(i, j)
            iq.read_data(i)
            iq.get_data(i,j)
    iq.close()
    print('*************************DONE**************************')