# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan

"""exec chariot with tclsh"""

from time import localtime
import os
import win32gui
from win32.lib import win32con
import threading
import pythoncom
import win32com.client
import logging
LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def chariot():
    # pythoncom.CoInitialize()
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where name ="tclsh.exe"')
    if len(processCodeCov) > 0:
        os.system('TASKKILL /F /IM tclsh.exe')
    directory = os.path.exists(r'./config')
    if directory is False:
        os.chdir(r'..')
        retval = os.getcwd()
        logging.info('before run rvr_chariot and set back to rvr:{0}'.format(retval))
    os.chdir(r'./config')
    retval = os.getcwd()
    logging.info('set chariot path and check:.{0}'.format(retval))
    logging.info('chariot start runing at    :{0}'.format(localtime()))
    os.system('tclsh rvr_chariot.tcl')
    os.chdir(r'..')
    retval = os.getcwd()
    logging.info('back to rvr path:{0}'.format(retval))


if __name__ == "__main__":
    chariot()
