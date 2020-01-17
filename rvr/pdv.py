# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan
# @FileName: pdv.py

# import serial
#
#
# class PDV:
#     def __init__(self, port):
#         self.port = port
#         self.instance = serial.Serial(port=self.port, baudrate=57600, bytesize=8, stopbits=1, timeout=2)
#         self.instance.timeout = 0.5
#         #print(self.instance.name, self.instance.port)
#
#     def send_cmd(self, cmd):
#         print(cmd)
#         cmd_list = []
#         for i in cmd:
#             cmd_list.append(i)
#             print(i,cmd_list)
#         for j in cmd_list:
#             cmd_exec_list = hex(j)
#             print(j,cmd_exec_list)
#             self.instance.write(cmd_exec_list.encode('ascii'))
#             response = self.instance.readline()
#             print('1',response)
#             response = self.convert_hex(response)
#             print('2',response)
#
#     def close(self):
#         self.instance.close()
#
#     def convert_hex(self, string):
#         res = []
#         result = []
#         for item in string:
#             res.append(item)
#         for i in res:
#             result.append(hex(i))
#             #print(result)
#         return result
#
# if __name__ == '__main__':
#     pdv = PDV('COM3')
#     #pdv.open()
#     #pdv.read_status()
#     #pdv.sets()
#     #print('SX0;'.encode('ascii'))
#     pdv.send_cmd('SX0;'.encode('ascii'))
#     pdv.send_cmd('DX128000;'.encode('ascii'))
#     pdv.send_cmd('MX4096;'.encode('ascii'))
#     pdv.send_cmd('JD3;'.encode('ascii'))
#     pdv.send_cmd('JL3000;'.encode('ascii'))
#     pdv.send_cmd('JW128000;'.encode('ascii'))
#     pdv.send_cmd('JW0;'.encode('ascii'))
#     pdv.send_cmd('JW0;'.encode('ascii'))
#     pdv.send_cmd('JW0;'.encode('ascii'))
#     pdv.send_cmd('JT0;'.encode('ascii'))
#     #pdv.send_cmd('UX;')
#     #pdv.send_cmd('US;')
#     #pdv.send_cmd('PA;')
#
#     pdv.close()

# import os
# main = "D:\work\Reamon\TP\OTA_RVR_TEST_TOOL\common\Emachine\Controller.exe"
# r_v = os.system(main)

# import subprocess
# import os
# main = "D:\work\Reamon\TP\OTA_RVR_TEST_TOOL\common\Emachine\Controller.exe"
# if os.path.exists(main):
#    rc,out= subprocess.getstatusoutput(main)
#    print (rc)
#    print ('*'*10)
#

# import os
# main = "D:\work\Reamon\TP\OTA_RVR_TEST_TOOL\common\Emachine\Controller.exe"
# f = os.popen(main)
# data = f.readlines()
# f.close()

import os
import time
import win32com.client
from ctypes import *
import logging

logger = logging.getLogger()


def Controller():
    # pythoncom.CoInitialize()
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where name ="Controller.exe"')
    if len(processCodeCov) > 0:
        logger.info("PDV Controller.exe process has been existed,now killed them!")
        os.system('TASKKILL /F /IM Controller.exe')
    try:
        os.chdir('./swiveltable')
        os.system('start Controller.exe')
    except:
        logger.error("Open MotorControl.exe failed!")
    time.sleep(3)
    for i in range(300, 500):
        windll.user32.SetCursorPos(900, i)
        windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.01)
        windll.user32.mouse_event(4, 0, 0, 0, 0)
        windll.user32.SetCursorPos(800, i)
    logger.info("Clockwise has been finished")
    os.system('TASKKILL /F /IM Controller.exe')
    os.chdir('..')


if __name__ == '__main__':
    Controller()
