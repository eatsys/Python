#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/5/6 13:38

__author__ = 'Ethan'

import telnetlib
import re
import logging
import config
conf = config.Config()
ap_ip = conf.Dutip_get()
username = conf.Username_get()
password = conf.Password_get()
radio = conf.Radio_get()
ap_type = conf.Ap_type_get()


class sta_rssi():
    def __init__(self, ap_ip, username, password, radio, ap_type):
        self.ip = ap_ip
        self.username = username
        self.password = password
        self.radio = radio
        self.ap_type = ap_type

    def login(self):
        try:
            tn = telnetlib.Telnet(self.ip, port=23, timeout=5)
            try:
                tn.read_until(b'Login:')
                tn.write(b'root')
                tn.read_until(b'Password:')
                tn.write(b'admin')
            except Exception as err:
                logging.info('No user', err)
        except Exception as err:
            logging.error('Connect fail', err)
        else:
            logging.info('Connect success!')

    def get_sta_RSSI(self):
        if self.ap_type == 'WF-194':
            self.tn.read_until(b'#')
            if self.radio == '2.4g':
                self.tn.write(b'wlanconfig ath0 list')
            else:
                self.tn.write(b'wlanconfig ath1 list')
            command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
            logging.info(command_result)
            command_result = re.search(b'\d+\r\n', command_result)
            logging.info(command_result)
            sta_rssi_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
            sta_linkrate_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
            logging.info(sta_rssi_value, sta_linkrate_value)
        elif self.ap_type == 'xxx':
            self.tn.read_until(b'#')
            if self.radio == '2.4g':
                self.tn.write(b'wlanconfig ath0 list')
            else:
                self.tn.write(b'wlanconfig ath1 list')
            command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
            logging.info(command_result)
            command_result = re.search(b'\d+\r\n', command_result)
            logging.info(command_result)
            sta_rssi_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
            sta_linkrate_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
            logging.info(sta_rssi_value, sta_linkrate_value)
        else:
            logging.info('No AP type')
