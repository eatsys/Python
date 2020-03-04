#!/user/bin/env python
# encoding: utf-8
# @time      : 2019/6/27 13:28

__author__ = 'Ethan'

"""for switch setting"""

from time import sleep
from data.parameters import RUN_TPYE
import telnetlib
import re
import logging
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理
#
# # 第二步，创建一个handler，用于写入日志文件
# file_handler = logging.FileHandler('./log/log.txt', mode='w')
# file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 创建该handler的formatter
# file_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# # 添加handler到logger中
# logger.addHandler(file_handler)
#
# # 第三步，创建一个handler，用于输出到控制台
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
# # 创建该handler的formatter
# console_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# logger.addHandler(console_handler)


class Switch:
    def __init__(self, ip):
        self.tn = telnetlib.Telnet(ip)
        self.tn.set_debuglevel(1)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def set_switch_sta(self, switch_port):
        port = 'A'
        if switch_port == '1':
            port = 'A'
        elif switch_port == '2':
            port = 'B'
        elif switch_port == '3':
            port = 'C'
        elif switch_port == '4':
            port = 'D'
        else:
            logger.error('Please check your switch port')
        sleep(2)
        self.tn.write(b'SET%s=1' % port.encode('ascii') + b'\n')
        command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
        logger.debug(command_result)
        command_result = re.search(b'\d+\n\r', command_result)
        logger.debug(command_result)
        status_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
        logger.debug(status_value)
        self.tn.write(b'SWPORT?' + b'\n')
        command_result = self.tn.read_until(b'\d+\n\r', timeout=1)
        logger.debug(command_result)
        command_result = re.search(b'([1-9]\d*\.?\d*)|(0\.\d*[0-9])\n\r', command_result)
        logger.debug(command_result)
        set_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
        if status_value == '1':
            logger.info('Switch Settings Successful! Value=%s' % set_value)
        else:
            logger.info('Switch Settings Fail')

    def set_switch_runtype(self):
        port_list = ['A', 'B', 'C', 'D']
        for port in port_list:
            if RUN_TPYE == 1:
                logger.info('Conductive')
                self.tn.write(b'SET%s=1' % port.encode('ascii') + b'\n')
                command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
                logger.debug(command_result)
                command_result = re.search(b'\d+\n\r', command_result)
                logger.debug(command_result)
                status_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                logger.debug(status_value)
                counts = 0
                while status_value == '0':
                    sleep(2)
                    self.tn.write(b'SET%s=1' % port.encode('ascii') + b'\n')
                    command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
                    logger.debug(command_result)
                    command_result = re.search(b'\d+\n\r', command_result)
                    logger.debug(command_result)
                    status_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                    logger.debug(status_value)
                    counts += 1
                    if counts > 5:
                        logger.info('Switch Settings Fail')
                        break
                else:
                    self.tn.write(b'SWPORT?' + b'\n')
                    command_result = self.tn.read_until(b'\d+\n\r', timeout=1)
                    logger.debug(command_result)
                    command_result = re.search(b'([1-9]\d*\.?\d*)|(0\.\d*[0-9])\n\r', command_result)
                    logger.debug(command_result)
                    set_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                    logger.info('Switch Settings Successful! Value=%s' % set_value)
            else:
                logger.info('OTA')
                self.tn.write(b'SET%s=0' % port.encode('ascii') + b'\n')
                command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
                logger.debug(command_result)
                command_result = re.search(b'\d+\n\r', command_result)
                logger.debug(command_result)
                status_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                logger.debug(status_value)
                counts = 0
                while status_value == '0':
                    sleep(2)
                    self.tn.write(b'SET%s=0' % port.encode('ascii') + b'\n')
                    command_result = self.tn.read_until(b'\d+\r\n', timeout=1)
                    logger.debug(command_result)
                    command_result = re.search(b'\d+\n\r', command_result)
                    logger.debug(command_result)
                    status_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                    logger.debug(status_value)
                    counts += 1
                    if counts > 5:
                        logger.info('Switch Settings Fail')
                        break
                else:
                    self.tn.write(b'SWPORT?' + b'\n')
                    command_result = self.tn.read_until(b'\d+\n\r', timeout=1)
                    logger.debug(command_result)
                    command_result = re.search(b'([0-9]\d*\.?\d*)|(0\.\d*[0-9])\n\r', command_result)
                    logger.debug(command_result)
                    set_value = re.sub('\n\r', '', command_result.group().decode('ascii'))
                    logger.info('Switch Settings Successful! Value=%s' % set_value)

    def set_default(self):
        self.tn.write(b'SETA=0' + b'\n')
        sleep(1)
        self.tn.write(b'SETB=0' + b'\n')
        sleep(1)
        self.tn.write(b'SETC=0' + b'\n')
        sleep(1)
        self.tn.write(b'SETD=0' + b'\n')
        sleep(1)


if __name__ == '__main__':
    swt = Switch('192.168.100.41')
    swt.set_default()
    #swt.set_switch_sta('4')
    swt.set_switch_runtype()
    swt.close()
