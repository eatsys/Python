#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author:Ethan


from __future__ import division
import visa
import pandas as pd
import time
from colorama import init, Fore, Style
import csv

init(autoreset=True)
dut_file = csv.reader(open('./config.csv'))
for rows in dut_file:
    if rows[0] == 'log_enable':
        le = rows[1]
        #print('Print Log: ', le)
    elif rows[0] == 'sleep_time':
        st = rows[1]
        #print('Sleep time: ', st)
    elif rows[0] == 'IQ_Port':
        iq_port = rows[1]
        # print('Sleep time: ', st)
    elif rows[0] == 'IQ_Rout':
        iq_rout = rows[1]
        # print('Sleep time: ', st)

log_switch = int(le)
sleep_time = float(st)

class IQxel():
    def __init__(self, ip, visaDLL=None, *args):
        self.ip = ip
        #self.visaDLL = 'C:\windows\system32\visa64.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::hislip0::INSTR' % self.ip
        #self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def __format__(self, format_spec):
        self.format_spec = format_spec
        format_spec = float(format_spec)
        format_spec = '{:.3f}'.format(format_spec)
        return format_spec

    def __log__(self,switch,log):
        if switch == 1:
            print(log)
        else:
            #print('no log')
            pass

    def __isset__(self,v):
        try:
            type(eval(v))
        except:
            return 0
        else:
            return 1

    def save_image(self, imagname, fmt):
        assert fmt in ['jpg', 'png'], 'Invalid postfix of image'
        print('MMEM:STOR:IMAG "%s.%s"' % (imagname, fmt))
        self.instance.write('MMEM:STOR:IMAG "%s.%s"' % (imagname, fmt))

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

    def read_pathloss(self,get_freqs,get_chains):
        self.get_freqs = get_freqs
        self.get_chains = get_chains
        pathloss = pd.read_csv('./pathloss.csv')
        self.__log__(log_switch,pathloss)
        freqlist = pathloss['Frequency']
        #print(freqlist)
        lens = len(freqlist)
        #print(lens)
        for x in range(lens):
            #print(x)
            #print(pathloss.loc[x,'Frequency'])
            if get_freqs == pathloss.loc[x,'Frequency']:
                loss = pathloss.loc[x]  #get frequency loss list
                print(loss)
                loss = loss[get_chains] #get chain loss value
                print('Channel:',get_freqs,'Chain:',get_chains,'pathloss:',loss)
                break
            else:
                pass
        return loss
        # freq = freqlist[0]
        # print (freq)
        # chaina = pathloss['1']
        # print(chaina)
        # chaina_2412 = chaina[0]
        # print (chaina_2412)
        # chainb = pathloss['2']
        # print(chainb)
        # chainb_2412 = chaina[0]
        # print(chaina_2412)
        # print(pathloss.loc[1, ['Frequency', '1','2','3','4']])
        # print(pathloss.loc[1, 'Frequency'])
        # print(pathloss.loc[1,'1'])
    def set_pathloss(self):
        pathloss = pd.read_csv('./pathloss.csv')
        self.__log__(log_switch, pathloss)
        freqlist = pathloss['Frequency']
        #print(freqlist)
        lens = len(freqlist)
        #print(lens)
        #creat loss table
        self.instance.write('MEM:TABLE "1"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x,'Frequency']
            loss = pathloss.loc[x,'1']
            #print(loss)
            self.instance.write('MEM:TABLE "1";MEMory:TABLe:INSert:POINt %f MHz,%f' %(channel,loss))
        self.instance.write('MEMory:TABLe "1";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "2"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x,'Frequency']
            loss = pathloss.loc[x,'2']
            #print(loss)
            self.instance.write('MEM:TABLE "2";MEMory:TABLe:INSert:POINt %f MHz,%f' %(channel,loss))
        self.instance.write('MEMory:TABLe "2";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "3"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x,'Frequency']
            loss = pathloss.loc[x,'3']
            #print(loss)
            self.instance.write('MEM:TABLE "3";MEMory:TABLe:INSert:POINt %f MHz,%f' %(channel,loss))
        self.instance.write('MEMory:TABLe "3";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "4"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x,'Frequency']
            loss = pathloss.loc[x,'4']
            #print(loss)
            self.instance.write('MEM:TABLE "4";MEMory:TABLe:INSert:POINt %f MHz,%f' %(channel,loss))
        self.instance.write('MEMory:TABLe "4";MEMory:TABLe:STORe')


    def read_data(self, target_power, mode, channel, chain):
        idns = self.instance.query('*IDN?')
        #print(idns)
        iq_port_model = iq_port.isdigit()
        #print(iq_port_model)
        iq_model = idns.split(',')
        #print(iq_model)
        iq_model = iq_model[1]
        #print(iq_model)
        if iq_model == 'IQXEL' and iq_port_model is True:
            mw = ''
        elif iq_model == 'IQXEL-M' and iq_port_model is False:
            mw = ''
        elif iq_model == 'IQXEL-MW' and iq_port_model is False:
            mw = 'M'
        #rint(mw, iq_rout, iq_port, iq_rout)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSA%s' % (mw, iq_rout, iq_port, iq_rout))
        self.instance.write('CHAN1;WIFI')
        channels = channel * 1000000
        self.instance.write('%sVSA%s;FREQ:cent %d' % (mw, iq_rout, channels))
        self.instance.write('%sVSA%s;SRAT 160000000' % (mw, iq_rout))
        #self.instance.write('VSA1 ;RLEVel:AUTO')
        rlevel = target_power + 15
        #print(rlevel)
        time.sleep(sleep_time)
        self.instance.write('%sVSA%s;RLEV %d;*wai;*opc?' % (mw, iq_rout, rlevel))
        self.instance.write('%sVSA%s;RFC:USE "%s",RF%s' % (mw, iq_rout, chain, iq_port))
        self.instance.write('%sVSA%s;RFC:STAT  ON,RF%s' % (mw, iq_rout, iq_port))
        #self.__log__(log_switch, chain)

        if mode == '11b':
            #print('DSSS')
            self.instance.write('CHAN1;WIFI;CONF:STAN DSSS')
            self.instance.write('VSA1;CAPT:TIME 0.03')
            self.instance.write('CHAN1')
            self.instance.write('VSA1 ;init')
            self.instance.write('WIFI')
            self.instance.write('calc:pow 0, 3')
            self.instance.write('calc:txq 0, 3')
            self.instance.write('calc:ccdf 0, 3')
            self.instance.write('calc:ramp 0, 3')
            self.instance.write('calc:spec 0, 3')
            #print(rec)
            time.sleep(1)
            # power
            data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
            self.__log__(log_switch, data)
        else:
            # print('OFDM')
            self.instance.write('CHAN1;WIFI;CONF:STAN OFDM')
            self.instance.write('CHAN1;WIFI;CONF:OFDM:CEST DATA')
            self.instance.write('VSA1;CAPT:TIME 0.005')
            self.instance.write('CHAN1')
            self.instance.write('VSA1 ;init')
            self.instance.write('WIFI')
            self.instance.write('calc:pow 0, 3')
            self.instance.write('calc:txq 0, 3')
            self.instance.write('calc:ccdf 0, 3')
            self.instance.write('calc:ramp 0, 3')
            self.instance.write('calc:spec 0, 3')
            data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
            self.__log__(log_switch, data)

            
    def get_data(self, mode, channel, rate, chain, result_name, target_power, spec_pwr, spec_evm, evm_margin,
                 spec_symbol_clock_error, spec_lo_leakage, spec_mask, spec_obw_20M, spec_obw_40M):
        if mode == '11b':
            data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
                avg_power = ''
                result_pwr = 'Fail'
            else:
                # self.__log__(log_switch, data)
                avg_power = data[1]
                # print(avg_power)
                avg_power = self.__format__(avg_power)
                delta_pwr = abs(float(avg_power) - target_power)
                #print(delta_pwr)
                #spec_pwr = 2
                if delta_pwr > spec_pwr:
                    print('Power:               ', Fore.RED+avg_power+Style.RESET_ALL, 'dBm')
                    result_pwr = 'Fail'
                else:
                    print('Power:               ', Fore.BLUE+avg_power+Style.RESET_ALL, 'dBm')
                    result_pwr = 'Pass'
            # txquality
            data = self.instance.query('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)#
            #print(datalen)
            data = data.split(',')
            if datalen < 20:
                print('Error', data)
                avg_evm = ''
            else:
                avg_evm = data[1]
                avg_evm = self.__format__(avg_evm)
                peak_evm = data[2]
                peak_evm = self.__format__(peak_evm)
                freq_error = data[4]
                freq_error = self.__format__(freq_error)
                peak_freq_error = data[5]
                peak_freq_error = self.__format__(peak_freq_error)
                symbol_clock_error = data[6]
                symbol_clock_error = self.__format__(symbol_clock_error)
                lo_leakage = data[7]
                lo_leakage = self.__format__(lo_leakage)
                #rate = rate + 'EVM'
                spec_evm = spec_evm - evm_margin
                if float(avg_evm) > spec_evm:
                    print('EVM:                 ', Fore.RED+avg_evm+Style.RESET_ALL, 'dB')
                    result_evm = 'Fail'
                else:
                    print('EVM:                 ', Fore.BLUE+avg_evm+Style.RESET_ALL, 'dB')
                    result_evm = 'Pass'
                print('EVM Peak:            ', peak_evm, 'dB')
                print('Frequency Error:     ', freq_error, 'kHz')
                print('Frequency Error Peak:', peak_freq_error, 'kHz')
                #spec_symbol_clock_error = eval('target_evm_'+rate)
                if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                    print('Symbol Clock Error:  ', Fore.RED + symbol_clock_error + Style.RESET_ALL, 'ppm')
                    result_symbol_clock_error = 'Fail'
                else:
                    print('Symbol Clock Error:  ', Fore.BLUE + symbol_clock_error + Style.RESET_ALL, 'ppm')
                    result_symbol_clock_error = 'Pass'
                #spec_lo_leakage = -15
                if abs(float(lo_leakage)) < abs(float(spec_lo_leakage)):
                    print('LO Leakage:          ', Fore.RED + lo_leakage + Style.RESET_ALL, 'dB')
                    result_lo_leakage = 'Fail'
                else:
                    print('LO Leakage:          ', Fore.BLUE + lo_leakage + Style.RESET_ALL, 'dB')
                    result_lo_leakage = 'Pass'
            # mask
            data = self.instance.query('WIFI;FETC:SEGM:SPEC:AVER:VIOL?')
            status = self.instance.query('*opc?')
            status = status.split(',')
            status = status[0]
            self.__log__(log_switch, status)
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                #self.__log__(log_switch, data)
                mask = data[1]
                mask = self.__format__(mask)
                #spec_mask = 5.12
                if abs(float(mask)) > spec_mask:
                    print('Mask:                ', Fore.RED + mask + Style.RESET_ALL, '%')
                    result_mask = 'Fail'
                else:
                    print('Mask:                ', Fore.BLUE + mask + Style.RESET_ALL, '%')
                    result_mask = 'Pass'
            # OBW
            data = self.instance.query('WIFI;FETC:SEGM:SPEC:AVER:OBW?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                #self.__log__(log_switch, data)
                obw = data[1]
                obw = self.__format__(obw)
                obw = round(float(obw)/1000000,3)
                spec_obw = spec_obw_20M
                if obw > spec_obw:
                    print('OBW:                 ', Fore.RED + str(obw) + Style.RESET_ALL, 'MHz')
                    result_obw = 'Fail'
                else:
                    print('OBW:                 ', Fore.BLUE + str(obw) + Style.RESET_ALL, 'MHz')
                    result_obw = 'Pass'
            # RAMP
            # on time
            data = self.instance.query('WIFI;FETC:SEGM:RAMP:ON:TRIS?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                # self.__log__(log_switch, data)
                ramp_on_time = data[1]
                ramp_on_time = float(ramp_on_time)*1000000
                ramp_on_time = self.__format__(ramp_on_time)
                spec_ramp_on_time = 2.0
                if float(ramp_on_time) > spec_ramp_on_time:
                    print('Ramp On Time:        ', Fore.RED + ramp_on_time + Style.RESET_ALL, 'us')
                    result_ramp_on_time = 'Fail'
                else:
                    print('Ramp On Time:        ', Fore.BLUE + ramp_on_time + Style.RESET_ALL, 'us')
                    result_ramp_on_time = 'Pass'
            #off time
            data = self.instance.query('WIFI;FETC:SEGM:RAMP:OFF:TRIS?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                # self.__log__(log_switch, data)
                ramp_off_time = data[1]
                ramp_off_time = float(ramp_off_time) * 1000000
                ramp_off_time = self.__format__(ramp_off_time)
                spec_ramp_off_time = 2.0
                if float(ramp_off_time) > spec_ramp_off_time:
                    print('Ramp Off Time:       ', Fore.RED + ramp_off_time + Style.RESET_ALL, 'us')
                    result_ramp_off_time = 'Fail'
                else:
                    print('Ramp Off Time:       ', Fore.BLUE + ramp_off_time + Style.RESET_ALL, 'us')
                    result_ramp_off_time = 'Pass'
            flatness = 'NA'
            spec_flatness = 'NA'
            result_flatness = 'NA'

        else:
            #print('OFDM')
            data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            #time.sleep(2)
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            self.__log__(log_switch, datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
                avg_power = ''
            else:
                self.__log__(log_switch, data)
                avg_power = data[1]
                avg_power = self.__format__(avg_power)
                delta_pwr = abs(float(avg_power) - target_power)
                #print(delta_pwr)
                ##spec_pwr = 2
                if delta_pwr > spec_pwr:
                    print('Power:               ', Fore.RED + avg_power + Style.RESET_ALL, 'dBm')
                    result_pwr = 'Fail'
                else:
                    print('Power:               ', Fore.BLUE + avg_power + Style.RESET_ALL, 'dBm')
                    result_pwr = 'Pass'
            # txquality
            data = self.instance.query('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 20:
                print('Error', data)
                avg_evm = ''
            else:
                self.__log__(log_switch,data)
                avg_evm = data[1]
                avg_evm = self.__format__(avg_evm)
                freq_error = data[3]
                freq_error = self.__format__(freq_error)
                symbol_clock_error = data[4]
                symbol_clock_error = self.__format__(symbol_clock_error)
                lo_leakage = data[5]
                lo_leakage = self.__format__(lo_leakage)
                spec_evm = spec_evm - abs(evm_margin)
                #print(spec_evm)
                if float(avg_evm) > spec_evm:
                    print('EVM:                 ', Fore.RED + avg_evm + Style.RESET_ALL, 'dB')
                    result_evm = 'Fail'
                else:
                    print('EVM:                 ', Fore.BLUE + avg_evm + Style.RESET_ALL, 'dB')
                    result_evm = 'Pass'
                print('Frequency Error:     ', freq_error, 'kHz')
                #spec_symbol_clock_error = 10.0
                if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                    print('Symbol Clock Error:  ', Fore.RED + symbol_clock_error + Style.RESET_ALL, 'ppm')
                    result_symbol_clock_error = 'Fail'
                else:
                    print('Symbol Clock Error:  ', Fore.BLUE + symbol_clock_error + Style.RESET_ALL, 'ppm')
                    result_symbol_clock_error = 'Pass'
                #spec_lo_leakage = -15
                if abs(float(lo_leakage)) < abs(float(spec_lo_leakage)):
                    print('LO Leakage:          ', Fore.RED + lo_leakage + Style.RESET_ALL, 'dB')
                    result_lo_leakage ='Fail'
                else:
                    print('LO Leakage:          ', Fore.BLUE + lo_leakage + Style.RESET_ALL, 'dB')
                    result_lo_leakage = 'Pass'
            # mask
            data = self.instance.query('WIFI;FETC:SEGM:SPEC:AVER:VIOL?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                # self.__log__(log_switch, data)
                mask = data[1]
                mask = self.__format__(mask)
                #spec_mask = 5.12
                if abs(float(mask)) > spec_mask:
                    print('Mask:                ', Fore.RED + mask + Style.RESET_ALL, '%')
                    result_mask = 'Fail'
                else:
                    print('Mask:                ', Fore.BLUE + mask + Style.RESET_ALL, '%')
                    result_mask = 'Pass'
            # OBW
            data = self.instance.query('WIFI;FETC:SEGM:SPEC:AVER:OBW?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                # self.__log__(log_switch, data)
                obw = data[1]
                obw = self.__format__(obw)
                obw = round(float(obw) / 1000000, 3)
                if mode == '11ng40plus':
                    spec_obw = spec_obw_40M
                else:
                    spec_obw = spec_obw_20M
                if obw > spec_obw:
                    print('OBW:                 ', Fore.RED + str(obw) + Style.RESET_ALL, 'MHz')
                    result_obw = 'Fail'
                else:
                    print('OBW:                 ', Fore.BLUE + str(obw) + Style.RESET_ALL, 'MHz')
                    result_obw = 'Pass'
            # flatness
            #datas = self.instance.query('FETC:SEGM1:OFDM:SFL:SIGN1:AVER?')
            #time.sleep(sleep_time)
            #time.sleep(10)
            #print('flatness', datas)
            data = self.instance.query('WIFI;FETC:SEGM:OFDM:SFL:AVER:CHEC?')
            status = self.instance.query('*opc?')
            self.__log__(log_switch, status)
            status = status.split(',')
            status = status[0]
            while status == '0':
                print('...')
                status = self.instance.query('*opc?')
                status = status.split(',')
                status = status[0]
            time.sleep(sleep_time)
            self.__log__(log_switch, data)
            datalen = len(data)
            # print(datalen)
            data = data.split(',')
            if datalen < 3:
                print('Error', data)
            else:
                # self.__log__(log_switch, data)
                flatness = data[0]
                spec_flatness = 0
                if int(flatness) == spec_flatness:
                    print('Flatness:            ', Fore.BLUE + flatness + Style.RESET_ALL)
                    result_flatness = 'Pass'
                else:
                    print('Flatness:            ', Fore.RED + flatness + Style.RESET_ALL)
                    result_flatness = 'Fail'
            ramp_on_time = 'NA'
            spec_ramp_on_time = 'NA'
            result_ramp_on_time = 'NA'
            ramp_off_time = 'NA'
            spec_ramp_off_time = 'NA'
            result_ramp_off_time = 'NA'

        #if mode == '11b' or mode == '11g':
        #    rates = 'M'
        #    rate = rate+rates
        #else:
        #    rates = 'MCS'
        #    rate = rates+rate
        #rate = mode+'_'+rate
        with open('./Result/' + result_name, 'a+', newline='') as f:
            writer = csv.writer(f)
            if avg_power == '' or avg_evm == '':
                pass
            else:
                writer.writerow([channel, rate, chain, target_power, avg_power, spec_pwr, result_pwr, avg_evm,
                                 spec_evm, result_evm, symbol_clock_error, spec_symbol_clock_error,
                                 result_symbol_clock_error, lo_leakage, spec_lo_leakage, result_lo_leakage, obw,
                                 spec_obw, result_obw,mask, spec_mask, result_mask, flatness, spec_flatness,
                                 result_flatness, ramp_on_time, spec_ramp_on_time, result_ramp_on_time,
                                 ramp_off_time, spec_ramp_off_time, result_ramp_off_time])

        return result_pwr, result_evm, result_symbol_clock_error, result_lo_leakage, result_mask, result_flatness

if __name__ == '__main__':
    iq = IQxel('192.168.100.253')
    iq.open()
    iq.read_idn()
    iq.init()
    #iq.read_pathloss(2462,2)
    iq.set_pathloss()
    iq.read_data(20, '11b', 2412, 1)
    iq.get_data('11b', 2412, '1M', 1, 'SN1', 20, 2, -10, 0, 10, 15, 0, 18, 38)
    iq.close()
    pass