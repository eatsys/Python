#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/25 15:31
"""remote to the station and exec the rssi.exe to get the ap's RSSI and link rate through ssh"""
__author__ = 'Ethan'

import os
import paramiko
import logging
from time import sleep
from data.parameters import AP_TYPE, RADIO, SSID

logger = logging.getLogger()


def get_rssi(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=22, username=username, password=password)
    ssh.exec_command(b'echo %s>ssid.txt' % SSID.encode('ascii'))
    sleep(1)
    ssh.exec_command(b'rssi.exe' + b'\r\n')
    sleep(10)
    ssh.close()

    retval = os.getcwd()
    file_path = retval + '/Result/Data/' + AP_TYPE + '_' + RADIO + '/'
    file_name = 'result.txt'
    transport = paramiko.Transport(host, 22)
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.get(file_name, file_path+file_name)  # 将remove_path 下载到本地 local_path
        transport.close()
    except Exception as err:
        logger.info('GET RSSI AND LINKRATE Failed', err)
    else:
        with open(file_path + file_name, 'r') as f:
            results = f.readlines()
            rssi = results[0]
            link_rate = results[2]
        return rssi, link_rate


if __name__ == "__main__":
    RSSI, LINKRATE = get_rssi('192.168.10.20', 'STA', 'DVT1.rf')
    print(RSSI, LINKRATE)
