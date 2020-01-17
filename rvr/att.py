# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan

"""for attenuate setting"""

import telnetlib
import re
import logging
logger = logging.getLogger()


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
        command_result = self.tn.read_until(b'\d+\r\n', timeout=2)
        logger.debug(command_result)
        command_result = re.search(b'\d+\r\n', command_result)
        logger.debug(command_result)
        status_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
        logger.debug(status_value)
        self.tn.write(b'ATT?' + b'\n')
        command_result = self.tn.read_until(b'\d+\r\n', timeout=2)
        logger.debug(command_result)
        command_result = re.search(b'([1-9]\d*\.?\d*)|(0\.\d*[0-9])\r\n', command_result)
        logger.debug(command_result)
        set_value = re.sub('\r\n', '', command_result.group().decode('ascii'))
        if status_value == '1':
            logger.info('Attenuation Settings Successful! Value=%s' % set_value)
        else:
            logger.info('Attenuation Settings Fail')

    def set_default(self):
        self.tn.write(b'SETATT=0' + b'\n')


if __name__ == '__main__':
    value = 0
    att = Attenuate('192.168.66.100')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.101')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.102')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.103')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.104')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.105')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.106')
    att.set_default()
    att.set_att(value)
    att.close()
    att = Attenuate('192.168.66.107')
    att.set_default()
    att.set_att(value)
    att.close()
