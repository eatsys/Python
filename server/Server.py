#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/29 10:07

__author__ = 'Ethan'

# 导入模块
import os
import socket
# 创建tcp服务端socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口
tcp_server_socket.bind(("", 8080))
# 设置监听，把服务端socket由主动套接字改成被动套接字，只能接收客户端的连接请求
tcp_server_socket.listen(128)
while True:
    # 接收客户端信息
    client_socket, client_ip = tcp_server_socket.accept()
    print("Client：", client_ip, "Connected")
    # 接收下载信息
    file_name_data = client_socket.recv(1024)
    # 解码下载信息
    file_name = file_name_data.decode()
    # get file path
    retval = os.getcwd() + '/'
    print('File Path', retval+file_name)
    file_path = retval
    try:
        # 数据传输
        with open(file_path + file_name, "rb") as file:
            while True:
                # 读取文件数据
                file_data = file.read(1024)
                # 数据长度不为0表示还有数据没有写入
                if file_data:
                    client_socket.send(file_data)
                # 数据为0表示传输完成
                else:
                    print(file_name, "Transported")
                    break
    except Exception as e:
        print("Error：", e)
    # 关闭客户端连接
    client_socket.close()