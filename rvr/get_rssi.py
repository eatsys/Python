#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/25 15:31
"""remote to the station and exec the rssi.exe to get the ap's RSSI and link rate"""
__author__ = 'Ethan'

import os
import telnetlib
from time import sleep
from data.parameters import SSID
import logging

LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

debug_switch = 1


class get_rssi():
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.tn.set_debuglevel(debug_switch)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def login(self, host, username, password):
        self.tn.open(host, port=23)
        sleep(5)
        #self.tn.read_until(b'(y/n): ', timeout=1)
        #self.tn.write(b'y' + b'\n')
        self.tn.read_until(b'login: ', timeout=1)
        self.tn.write(username.encode('ascii') + b'\r\n')
        self.tn.read_until(b'password: ', timeout=1)
        self.tn.write(password.encode('ascii') + b'\r\n')
        self.tn.read_until(b'FDP00241>', timeout=1)
        self.tn.write(b'dir' + b'\r\n')
        sleep(2)

    def creat_ssid(self):
        self.tn.read_until(b'FDP00241>', timeout=1)
        self.tn.write(b'echo %s>ssid.txt' % SSID.encode('ascii'))

    def get_rssi_value(self):
        self.tn.write(b'\r\n')
        self.tn.read_until(b'FDP00241>', timeout=1)
        self.tn.write(b'start rssi.exe' + b'\r\n')
        sleep(10)
        self.tn.read_until(b'FDP00241>', timeout=1)
        self.tn.write(b'type result.txt' + b'\r\n')
        #command_result = self.tn.read_very_eager().decode('ascii')
        #print('\n%s' % command_result)
        #file = 'result.txt'
        #with open(file, 'r') as f:
        #    result = f.read()
        #    print(result)


if __name__ == "__main__":
    get = get_rssi()
    get.login('192.168.1.111', 'FDP00241', 'DVT1.rf')
    get.creat_ssid()
    get.get_rssi_value()