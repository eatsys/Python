# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx_test.py

from __future__ import division
from openpyxl import load_workbook
import visa
import telnetlib
import pandas as pd
import time
import datetime
from colorama import init, Fore, Style
import csv
import re
import logging

class IQxel():
    def __init__(self, ip, visaDLL=None, *args):
        self.ip = ip
        # self.visaDLL = 'C:\windows\system32\visa64.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::hislip0::INSTR' % self.ip
        # self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.resourceManager = visa.ResourceManager()

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def __formats__(self, format_spec):
        self.format_spec = format_spec
        format_spec = float(format_spec)
        format_spec = '{:.3f}'.format(format_spec)
        return format_spec

    def __log__(self, switch, log):
        if switch == 1:
            print(log)
        else:
            # print('no log')
            pass

    def __isset__(self, v):
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
        # return idn

    def init(self):
        self.instance.write('ROUT1;PORT:RES RF1,OFF')
        self.instance.write('ROUT1;PORT:RES RF2,OFF')

        # print('iq init...')

    def read_pathloss(self, get_freqs, get_chains):
        self.get_freqs = get_freqs
        self.get_chains = get_chains
        pathloss = pd.read_csv('./pathloss.csv')
        self.__log__(log_switch, pathloss)
        freqlist = pathloss['Frequency']
        # print(freqlist)
        lens = len(freqlist)
        # print(lens)
        for x in range(lens):
            # print(x)
            # print(pathloss.loc[x,'Frequency'])
            if get_freqs == pathloss.loc[x, 'Frequency']:
                loss = pathloss.loc[x]  # get frequency loss list
                print(loss)
                loss = loss[get_chains]  # get chain loss value
                print('Channel:', get_freqs, 'Chain:', get_chains, 'pathloss:', loss)
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
        # print(freqlist)
        lens = len(freqlist)
        # print(lens)
        # creat loss table
        self.instance.write('MEM:TABLE "1"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x, 'Frequency']
            loss = pathloss.loc[x, '1']
            # print(loss)
            self.instance.write('MEM:TABLE "1";MEMory:TABLe:INSert:POINt %f MHz,%f' % (channel, loss))
        self.instance.write('MEMory:TABLe "1";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "2"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x, 'Frequency']
            loss = pathloss.loc[x, '2']
            # print(loss)
            self.instance.write('MEM:TABLE "2";MEMory:TABLe:INSert:POINt %f MHz,%f' % (channel, loss))
        self.instance.write('MEMory:TABLe "2";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "3"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x, 'Frequency']
            loss = pathloss.loc[x, '3']
            # print(loss)
            self.instance.write('MEM:TABLE "3";MEMory:TABLe:INSert:POINt %f MHz,%f' % (channel, loss))
        self.instance.write('MEMory:TABLe "3";MEMory:TABLe:STORe')
        self.instance.write('MEM:TABLE "4"; MEM:TABLE:DEFINE "FREQ,LOSS"')
        for x in range(lens):
            channel = pathloss.loc[x, 'Frequency']
            loss = pathloss.loc[x, '4']
            # print(loss)
            self.instance.write('MEM:TABLE "4";MEMory:TABLe:INSert:POINt %f MHz,%f' % (channel, loss))
        self.instance.write('MEMory:TABLe "4";MEMory:TABLe:STORe')

    def read_data(self, target_power, channel, chain):
        idns = self.instance.query('*IDN?')
        # print(idns)
        iq_port_model = iq_port.isdigit()
        # print(iq_port_model)
        iq_model = idns.split(',')
        # print(iq_model)
        iq_model = iq_model[1]
        # print(iq_model)
        if iq_model == 'IQXEL' and iq_port_model is True:
            mw = ''
        elif iq_model == 'IQXEL-M' and iq_port_model is False:
            mw = ''
        elif iq_model == 'IQXEL-MW' and iq_port_model is False:
            mw = 'M'
        #print(mw, iq_rout, iq_port, iq_rout)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSA%s' % (mw, iq_rout, iq_port, iq_rout))
        self.instance.write('CHAN1;WIFI')
        channels = (channel*5 + 2407) * 1000000
        #print(channels)
        self.instance.write('%sVSA%s;FREQ:cent %d' % (mw, iq_rout, channels))
        self.instance.write('%sVSA%s;SRAT 160000000' % (mw, iq_rout))
        # self.instance.write('VSA1 ;RLEVel:AUTO')
        rlevel = target_power + 15
        # print(rlevel)
        time.sleep(sleep_time)
        self.instance.write('%sVSA%s;RLEV %d;*wai;*opc?' % (mw, iq_rout, rlevel))
        self.instance.write('%sVSA%s;RFC:USE "%s",RF%s' % (mw, iq_rout, chain, iq_port))
        self.instance.write('%sVSA%s;RFC:STAT  ON,RF%s' % (mw, iq_rout, iq_port))
        # self.__log__(log_switch, chain)
        self.instance.write('CHAN1;WIFI;CONF:STAN OFDM')
        self.instance.write('CHAN1;WIFI;CONF:OFDM:CEST DATA')
        self.instance.write('VSA%s;CAPT:TIME 0.005' % iq_rout)
        self.instance.write('CHAN1')
        self.instance.write('VSA%s ;init' % iq_rout)
        self.instance.write('WIFI')
        self.instance.write('calc:pow 0, 3')
        self.instance.write('calc:txq 0, 3')
        self.instance.write('calc:ccdf 0, 3')
        self.instance.write('calc:ramp 0, 3')
        self.instance.write('calc:spec 0, 3')
        data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
        self.__log__(log_switch, data)

    def get_data(self):
        # print('OFDM')
        data = self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
        time.sleep(sleep_time)
        self.__log__(log_switch, data)
        data_len = len(data)
        self.__log__(log_switch, data_len)
        data = data.split(',')
        if data_len < 3:
            print('Error', data)
            avg_power = 'NA'
        else:
            self.__log__(log_switch, data)
            avg_power = data[1]
            avg_power = self.__formats__(avg_power)
            print('Power:', Fore.BLUE + avg_power + Style.RESET_ALL, 'dBm')
            avg_power = float(avg_power)*10
            avg_power = '{:.0f}'.format(avg_power)
        return avg_power

class dut():
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.tn.set_debuglevel(0)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def login(self, host, username, password):
        self.tn.open(host, port=23)
        time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        print(command_result)
        self.tn.read_until(b'Login: ', timeout=1)
        self.tn.write(username.encode('ascii') + b'\n')
        self.tn.read_until(b'Password:', timeout=1)
        self.tn.write(password.encode('ascii') + b'\n')

        time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        print(command_result)
        if 'wrong' not in command_result:
            logging.info('%s Sign up' % host)
            return True
        else:
            logging.warning('%s Login Fail' % host)
            return False

    def init(self, str1, str2, str3):
        self.tn.read_until(b'WAP>', timeout=1)
        self.tn.write(str1.encode('ascii') + b'\n')

        #set default
        self.tn.read_until(b'SU_WAP>', timeout=3)
        self.tn.write(b'wifi calibrate test parameter write wifichip 1 type power len 77 value default' + b'\n')
        self.tn.read_until(b'SU_WAP>', timeout=3)
        #self.tn.write(b'wifi calibrate test parameter write wifichip 2 type power len 155 value default' + b'\n')

        self.tn.read_until(b'SU_WAP>', timeout=3)
        self.tn.write(b'wifi calibrate test parameter write wifichip 1 type upc len 12 value default' + b'\n')
        self.tn.read_until(b'SU_WAP>', timeout=3)
        #self.tn.write(b'wifi calibrate test parameter write wifichip 2 type upc len 28 value default' + b'\n')


        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(str2.encode('ascii') + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(str3.encode('ascii') + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=3)
        self.tn.write(b'wifi_equipment.sh init chip 1' + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=3)
        #self.tn.write(b'wifi_equipment.sh init chip 2' + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txpower 300 ' + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'wifi_equipment.sh get_txpower chip 1 para 3' + b'\n')
        command_result = self.tn.read_until(b'success!', timeout=1)
        command_result = re.search(b'\d+,\d+,\d+', command_result)
        if command_result is None:
            power_list = [20, 16, 12]
        else:
            print(command_result)
            default_value = (command_result.group().decode('ascii')).split(',')
            power_list = default_value
        print(power_list)
        return power_list

    def ex_command(self, command):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.info('\n%s' % command_result)


    def tx(self, channel, chain):
        # for 2.4g
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txpower 300' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 mode 11g' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 bw 20' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 channel %d' % channel + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 rate 6' + b'\n')
        if chain == 0:
            chains = '01'
        else:
            chains = '10'
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txch 00%s' % chains.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 al_tx 1' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        print('TX COMMANDS DONE')

    def adjust_power(self, power):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txpower %d' % power + b'\n')

    def set_default(self):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txpower 300' + b'\n')

    def set_cal(self, chain, subband, pa, pb, pc):
        print(pa,pb,pc)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv Hisilicon0 cali_power "%d %d %d %d %d"' % (chain, subband, pa, pb, pc) + b'\n')
        print(b'iwpriv Hisilicon0 cali_power "%d %d %d %d %d"' % (chain, subband, pa, pb, pc))

    def cal(self):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 get_power_param' + b'\n')
        command_result = self.tn.read_until(b'success\r\n\r\n', timeout=1)
        command_result = re.search(b'\r\n\w+\r\nsuccess', command_result)
        #print(command_result)
        #print(command_result.group().decode('ascii'))
        command_result = re.sub('\r\n', '', command_result.group().decode('ascii'))
        command_result = re.sub('success', '', command_result)
        #print(command_result)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'exit' + b'\n')
        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(b'wifi calibrate test parameter write wifichip 1 type power len 77 value %s' %
                      command_result.encode('ascii') + b'\n')

        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(b'shell' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.write(b'iwpriv vap0 get_upc_param' + b'\n')
        command_result = self.tn.read_until(b'success\r\n\r\n', timeout=3)
        command_result = re.search(b'\r\n\w+\r\nsuccess', command_result)
        command_result = re.sub('\r\n', '', command_result.group().decode('ascii'))
        command_result = re.sub('success', '', command_result)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'exit' + b'\n')
        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(b'wifi calibrate parameter crc calc' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'wifi calibrate test parameter write wifichip 1 type upc len 12 value %s' %
                      command_result.encode('ascii') + b'\n')
        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(b'reset' + b'\n')

if __name__ == '__main__':
    init(autoreset=True)

    print('***********************************************************************************')
    print(Fore.LIGHTRED_EX + '校准只能在单板上电之后的初始状态执行，如果进行过任何WIFI命令相关操作，请重启后再执行校准操作!' + Style.RESET_ALL)
    print('***********************************************************************************')
    Number = input("SN:")
    sn = "SN_"+Number

    dut_file = csv.reader(open('./config.csv'))
    for rows in dut_file:
        if rows[0] == 'DUT_IP':
            dut_ip = rows[1]
            print('DUT IP: ', dut_ip)
        elif rows[0] == 'username':
            user = rows[1]
            print('DUT Username: ', user)
        elif rows[0] == 'password':
            pwd = rows[1]
            print('DUT Password: ', pwd)
        elif rows[0] == 'addition1':
            add1 = rows[1]
            print('Addition Parameters: ', add1)
        elif rows[0] == 'addition2':
            add2 = rows[1]
            print('Addition Parameters: ', add2)
        elif rows[0] == 'addition3':
            add3 = rows[1]
            print('Addition Parameters: ', add3)
        elif rows[0] == 'log_enable':
            le = rows[1]
            print('Print Log: ', le)
        elif rows[0] == 'sleep_time':
            st = rows[1]
            print('Sleep time: ', st)
        elif rows[0] == 'IQ_IP':
            iq_ip = rows[1]
            print('IQ IP: ', iq_ip)
        elif rows[0] == 'IQ_Port':
            iq_port = rows[1]
            print('IQ PORT: ', iq_port)
        elif rows[0] == 'IQ_Rout':
            iq_rout = rows[1]
            print('IQ ROUT: ', iq_rout)

    log_switch = int(le)
    sleep_time = float(st)
    chain_list = [0, 1]
    channel_list = [3, 8, 12]
    subband_list = [0, 1, 2]
    #INIT IQ
    iq = IQxel(iq_ip)
    iq.open()
    iq.read_idn()
    iq.reset()
    iq.set_pathloss()

    #INIT DUT
    dt = dut()
    dt.login(dut_ip, user, pwd)
    power_list = dt.init(add1, add2, add3)
    #print(power_list)
    mea_power = []
    for values in power_list:
        values = int(values) * 10
        mea_power.append(values)
    print(mea_power)

    #GEN Report
    now_time = datetime.datetime.now()
    now_time = str(now_time)
    now_time = now_time.split()
    day_time = re.sub('-', '', now_time[0])
    now_time = now_time[1].split('.')
    now_time = re.sub(':', '', now_time[0])
    now_time = day_time + now_time
    result_name = sn + '_' + 'TX_Result' + '_' + now_time + '.csv'
    with open('./Result/' + result_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['FREQ', 'DATA_RATE', 'CHAIN', 'TX_POWER', 'POWER', 'LIMIT', 'RESULT'])

    #cal
    print('*************************************************************')
    for chain in chain_list:
        for channel in channel_list:
            if channel == 3:
                subband = 0
            elif channel == 8:
                subband = 1
            elif channel == 12:
                subband = 2
            dt.tx(channel, chain)
            value_list = []
            for power in mea_power:
                print('Power', power, 'Channel:', channel, 'Chain:', chain)
                #TX
                dt.adjust_power(power)
                #RESULT
                iq.read_data(power, channel, chain)
                avg_power = iq.get_data()
                value_list.append(avg_power)
                print(value_list)
                print('*************************************************************')
            dt.set_default()
            value_list = list(map(int, value_list))
            print(chain, subband)
            dt.set_cal(chain, subband, value_list[0], value_list[1], value_list[2])
    dt.cal()
    dt.close()
    iq.close()