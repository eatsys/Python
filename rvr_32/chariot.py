# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan

"""exec chariot with tclsh"""

import logging
import os
from time import localtime

import pythoncom
import win32com.client

logger = logging.getLogger()


def chariot_tx():
    pythoncom.CoInitialize()
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where name ="tclsh.exe"')
    if len(processCodeCov) > 0:
        os.system('TASKKILL /F /IM tclsh.exe')
    directory = os.path.exists(r'./config')
    if directory is False:
        os.chdir(r'..')
        retval = os.getcwd()
        logger.info('before run rvr_chariot and set back to rvr:{0}'.format(retval))
    os.chdir(r'./config')
    retval = os.getcwd()
    logger.info('set chariot path and check:.{0}'.format(retval))
    logger.info('chariot start runing at    :{0}'.format(localtime()))
    os.system('tclsh rvr_chariot_tx.tcl')
    os.chdir(r'..')
    retval = os.getcwd()
    logger.info('back to rvr path:{0}'.format(retval))


def chariot_rx():
    pythoncom.CoInitialize()
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where name ="tclsh.exe"')
    if len(processCodeCov) > 0:
        os.system('TASKKILL /F /IM tclsh.exe')
    directory = os.path.exists(r'./config')
    if directory is False:
        os.chdir(r'..')
        retval = os.getcwd()
        logger.info('before run rvr_chariot and set back to rvr:{0}'.format(retval))
    os.chdir(r'./config')
    retval = os.getcwd()
    logger.info('set chariot path and check:.{0}'.format(retval))
    logger.info('chariot start runing at    :{0}'.format(localtime()))
    os.system('tclsh rvr_chariot_rx.tcl')
    os.chdir(r'..')
    retval = os.getcwd()
    logger.info('back to rvr path:{0}'.format(retval))


if __name__ == "__main__":
    chariot_tx()
    chariot_rx()
