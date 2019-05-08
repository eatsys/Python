#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/5/6 13:38

__author__ = 'Ethan'

import telnetlib
import config
conf = config.Config()
ap_ip = conf.Dutip_get()
username = conf.Username_get()
password = conf.Password_get()
radio = conf.Radio_get()
ap_type = conf.Ap_type_get()
import logging


class sta_rssi():
    def __init__(self, ap_ip, username, password, radio, ap_type):
        self.ip = ap_ip
        self.username = username
        self.password = password
        self.radio = radio
        self.ap_type = ap_type

    def get_sta_RSSI(self):
        if self.ap_type == 'WF-194':
            try:
                tn = telnetlib.Telnet(self.ip, port=23, timeout=5)
            except Exception as err:
                logging.error('Connect fail', err)
            else:
                tn.read_until(b'#')
                if self.radio == '2.4g':
                    tn.write(b'iwconfig ath0')
                else:
                    tn.write(b'iwconfig ath1')