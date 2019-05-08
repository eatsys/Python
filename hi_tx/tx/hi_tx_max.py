# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx.py

import logging
import time
import telnetlib
import re


class dut():
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.tn.set_debuglevel(1)

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

    def init(self,  str1,   str2,   str3):
        self.tn.read_until(b'WAP>', timeout=1)
        self.tn.write(str1.encode('ascii') + b'\n')

        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(str2.encode('ascii') + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(str3.encode('ascii') + b'\n')

        command_result = self.tn.read_very_eager().decode('ascii')
        logging.info('\n%s' % command_result)

    def ex_command(self, command):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.info('\n%s' % command_result)


    def tx(self,mode,channel,bw,rate,chain):
        # for 2.4g
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap0 down' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 setessid Hi24g' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 mode %s' % mode.encode('ascii') + b'\n')
        #print(channel)
        if bw == '40':
            channels = int(channel) - 10
            #print(channel)
        else:
            channels = channel
        channels = (int(channels)-2407)/5 #2407+5*1=2412
        #print(channel)
        channels = str(channels)
        #print(channel)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 channel %s' % channels.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 privflag 1' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 al_rx 0' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap0 2040bss_enable 0"' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap0 radartool enable 0"' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap0 acs sw 0"' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap0 up' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 al_tx 0' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        #self.tn.write(b'hipriv.sh "vap0 add_user 07:06:05:04:03:02 1"\r')
        self.tn.write(b'iwpriv vap0 bw %s' % bw.encode('ascii') + b'\n')
        if mode == '11b' or mode == '11g':
            rates = 'rate'
        else:
            rates = 'mcs'
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 %s ' % rates.encode('ascii') + b'%s' % rate.encode('ascii') + b'\n')
        if chain is '0':
            chains = '01'
        else:
            chains = '10'#
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txch 00%s' % chains.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 al_tx "1 2 1000 "' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        print('TX COMMANDS DONE')

        if int(channel) < 2437 and chain == '0':
            channel_groups = '98'
        elif int(channel) < 2437 and chain == '1':
            channel_groups = 'a8'
        elif 2437 < int(channel) < 2462 and chain == '0':
            channel_groups = '94'
        elif 2437 < int(channel) < 2462 and chain == '1':
            channel_groups = 'a4'
        elif int(channel) >= 2462 and chain == '0':
            channel_groups = '90'
        elif int(channel) >= 2462 and chain == '1':
            channel_groups = 'a0'

        self.tn.write(b'hipriv.sh "vap0 set_tx_pow rf_reg_ctl 1"' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap0 reginfo soc 0x200380%s 0x200380%s";dmesg -c'
                      % (channel_groups.encode('ascii'), channel_groups.encode('ascii')) + b'\n')
        #self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        #command_result = self.tn.read_very_eager().decode('ascii')
        command_result = self.tn.read_until(b'value=0x\w+\r\r\nWAP(Dopra Linux) # ', timeout=3)
        command_result = re.search(b'value=0x\w+', command_result)
        default_value = re.sub('value=0x', '', command_result.group().decode('ascii'))
        print('Default Value:', default_value)
        default_value = int(default_value, 16)
        #print(default_value)
        pwr_para = default_value + 2
        pwr_paras = hex(pwr_para)
        #print(pwr_paras)
        print(channel_groups, pwr_paras)
        return (channel_groups, pwr_paras)

    def adjust_power(self, channel_groups, pwr_paras):
        print('New Value:', pwr_paras)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap0 regwrite soc 0x200380%s 0x%s"'
                      % (channel_groups.encode('ascii'), pwr_paras.encode('ascii')) + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)

if  __name__=='__main__':
    #pass
    dt = dut()#
    dt.login('192.168.100.1','root','admin')
    dt.init('su', 'shell','')
    dt.tx('11g',2442,'20','54',1)
    dt.adjust_power(2442, 1)