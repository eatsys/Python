# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan

"""for attenuate setting"""

import telnetlib
import re
import logging

LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class Attenuate:
    def __init__(self, ip):
        self.tn = telnetlib.Telnet(ip)
        self.tn.set_debuglevel(1)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def set_att(self, attenuate_value):
        self.tn.write(b'SETATT=%d' % attenuate_value + b'\n')
        command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
        logging.info(command_result)
        command_result = re.search(b'\d+\r\n', command_result)
        logging.info(command_result)
        status_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
        logging.info(status_value)
        self.tn.write(b'ATT?' + b'\n')
        command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
        logging.info(command_result)
        command_result = re.search(b'([1-9]\d*\.?\d*)|(0\.\d*[0-9])\r\n', command_result)
        logging.info(command_result)
        set_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
        if status_value == '1':
            logging.info('Attenuation Settings Successful! Value=%s' % set_value)
        else:
            logging.info('Attenuation Settings Fail')

    def set_default(self):
        self.tn.write(b'SETATT=60' + b'\n')


if __name__ == '__main__':
    att = Attenuate('192.168.100.100')
    att.set_default()
    att.set_att(0)
    att.close()
