# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx.py

import telnetlib

def tx(ip,mode,channel,bw,rate,chain):
    # for 2.4g
    Host = ip
    Port = 23
    tn = telnetlib.Telnet(Host, Port, timeout=3)
    tn.set_debuglevel(0);
    tn.write(b'\r\n')
    tn.write('ifconfig vap0 down')
    tn.write('iwpriv vap0 setessid Hi24g')
    tn.write('iwpriv vap0 mode %s' % mode)
    tn.write('iwpriv vap0 channel %d' % channel)
    tn.write('iwpriv vap0 privflag 1 ')
    tn.write('iwpriv vap0 al_rx 0 ')
    tn.write('hipriv.sh "vap0 2040bss_enable 0"')
    tn.write('hipriv.sh "vap0 radartool enable 0" ')
    tn.write('hipriv.sh "vap0 acs sw 0" ')
    tn.write('ifconfig vap0 up ')
    tn.write('iwpriv vap0 al_tx 0 ')
    tn.write('hipriv.sh "vap0 add_user 07:06:05:04:03:02 1 "')
    tn.write('iwpriv vap0 bw %d ' % bw)
    if mode is '11b' or '11g':
        rates = 'rate'
    else:
        rates = 'mcs'
    tn.write('iwpriv vap0 %s ' % rates +'%d' % rate)
    tn.write('iwpriv vap0 txch %d' % chain)
    tn.write('iwpriv vap0 al_tx "1 2 1000 "')
    tn.close()


