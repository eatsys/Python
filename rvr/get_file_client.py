#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/29 9:45
"""download the ap's RSSI and link rate file from the station, open it and write the data to txt in local"""
__author__ = 'Ethan'

from data.parameters import STA_IP
import socket
import os
from config import conf
test_ap = conf.Ap_type_get()


def get_RSSI_file():
    # 创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口
    tcp_client_socket.bind(("", 8080))
    # 连接IP地址和端口
    tcp_client_socket.connect((STA_IP, 8080))
    retval = os.getcwd()
    #print('1111', retval)
    file_path = retval + '/Result/Data/ ' + test_ap + '/'
    file_name = 'result.txt'
    # 文件名编码
    tcp_client_socket.send(file_name.encode())

    try:
        # 文件传输
        with open(file_path + file_name, "wb") as file:
            while True:
                # 接收数据
                file_data = tcp_client_socket.recv(1024)
                # 数据长度不为0写入文件
                if file_data:
                    file.write(file_data)
                # 数据长度为0表示下载完成
                else:
                    break
    # 下载出现异常时捕获异常
    except Exception as e:
        print("Download Fail", e)
    # 无异常则下载成功
    else:
        print(file_name, "Download success!")
    # 关闭客户端
    tcp_client_socket.close()
    #os.rename(file_path+file_name, file_path+'rssi.txt')
    with open(file_path+file_name, 'r') as f:
        results = f.readlines()
        rssi = results[0]
        link_rate = results[2]
    return rssi, link_rate

if __name__ == "__main__":
    get_RSSI_file()
