# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx.py

import logging
import time
import telnetlib


class dut():
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.tn.set_debuglevel(0)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def login(self, host, username, password):
        #try:
        #    self.tn.open(host, port=23)
#
        #except:
        #    logging.warning('%s Connect failed' % host)
        #    return False
        self.tn.open(host, port=23)
        time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        print(command_result)
        self.tn.read_until(b'Login: ', timeout=1)
        self.tn.write(username.encode('ascii') + b'\n')
        self.tn.read_until(b'Password:', timeout=1)
        self.tn.write(password.encode('ascii') + b'\n')

        time.sleep(1)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        print('1',command_result)
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
            channel = int(channel) - 10
            #print(channel)
        else:
            channel = channel
        channel = (int(channel)-2407)/5 #2407+5*1=2412
        #print(channel)
        channel = str(channel)
        #print(channel)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 channel %s' % channel.encode('ascii') + b'\n')
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
            chain = '01'
        else:
            chain = '10'#
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 txch 00%s' % chain.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap0 al_tx "1 2 1000 "' + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        print('TX COMMANDS DONE')



if  __name__=='__main__':
    pass
    #dut_file = csv.reader(open('./dut_config.csv'))
    #for rows in dut_file:
    #    if rows[0] == 'ip':
    #        ip = rows[1]
    #        print('DUT IP: ', ip)
    #    elif rows[0] == 'username':
    #        user = rows[1]
    #        print('DUT Username: ', user)
    #    elif rows[0] == 'password':
    #        pwd = rows[1]
    #        print('DUT Password: ', pwd)
    #    elif rows[0] == 'addition1':
    #        add1 = rows[1]
    #        print('Addition Parameters: ', add1)
    #    elif rows[0] == 'addition2':
    #        add2 = rows[1]
    #        print('Addition Parameters: ', add2)
    #    elif rows[0] == 'addition3':
    #        add3 = rows[1]
    #        print('Addition Parameters: ', add3)
    #print('hh')
    #dt = dut()
    #dt.login(ip,user,pwd)
    #dt.init(add1,add2,add3)
    #dt.ex_command('ls')
    #dt.tx('11g',2442,'20','54',1)