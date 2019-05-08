# -*- coding:utf-8 -*-

"""for config file"""

__author__ = 'DVTRF'


import configparser
#import logging
#logging = logging.getlogging(__name__)
#logging.setLevel(level=logging.INFO)
# = logging.FileHandler("./log/log.txt")
#handler.setLevel(logging.INFO)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)
#logging.addHandler(handler)
import logging
LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

config_file = "./config/config.ini"


# 配置文件读取
class Config:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Ap_type_get(self):
        aptype = self.conf.get("ap_config", "ap_type")
        logging.info("ap type is     : {0}".format(aptype))
        return aptype

    def Dutip_get(self):
        dutip = self.conf.get("ap_config", "dut_ip")
        logging.info("dut ip is     : {0}".format(dutip))
        return dutip

    def Username_get(self):
        username = self.conf.get("ap_config", "username")
        logging.info("user name is     : {0}".format(username))
        return username

    def Password_get(self):
        password = self.conf.get("ap_config", "password")
        logging.info("password is     : {0}".format(password))
        return password

    def SSID_get(self):
        ssid = self.conf.get("ap_config", "ssid")
        logging.info("SSID is     : {0}".format(ssid))
        return ssid

    def Radio_get(self):
        radio = self.conf.get("ap_config", "radio")
        logging.info("radio is     : {0}".format(radio))
        return radio

    def Channel_get(self):
        channel = self.conf.get("ap_config", "channel")
        logging.info("channel is     : {0}".format(channel))
        return channel

    def Atten_start_get(self):
        atten_start = self.conf.get("atten_config", "atten_start")
        logging.info("atten start    : {0}".format(atten_start))
        return atten_start

    def Atten_end_get(self):
        atten_end = self.conf.get("atten_config", "atten_end")
        logging.info("atten end     : {0}".format(atten_end))
        return atten_end

    def Atten_step_get(self):
        atten_step = self.conf.get("atten_config", "atten_step")
        logging.info("atten step is     : {0}".format(atten_step))
        return atten_step

    def External_loss_get(self):
        external_loss = self.conf.get("atten_config", "external_loss")
        logging.info("external loss is     : {0}".format(external_loss))
        return external_loss

    def Atten_num_get(self):
        atten_num = self.conf.get("atten_config", "atten_num")
        logging.info("atten number is     : {0}".format(atten_num))
        return atten_num

    def Atten_1_ip_get(self):
        att_1_ip = self.conf.get("atten_config", "att_1_ip")
        logging.info("atten 1 ip is     : {0}".format(att_1_ip))
        return att_1_ip

    def Atten_2_ip_get(self):
        att_2_ip = self.conf.get("atten_config", "att_2_ip")
        logging.info("atten 2 ip is     : {0}".format(att_2_ip))
        return att_2_ip

    def Atten_3_ip_get(self):
        att_3_ip = self.conf.get("atten_config", "att_3_ip")
        logging.info("atten 3 ip is     : {0}".format(att_3_ip))
        return att_3_ip

    def Atten_4_ip_get(self):
        att_4_ip = self.conf.get("atten_config", "att_4_ip")
        logging.info("atten 4 ip is     : {0}".format(att_4_ip))
        return att_4_ip

    def Atten_5_ip_get(self):
        att_5_ip = self.conf.get("atten_config", "att_5_ip")
        logging.info("atten 5 ip is     : {0}".format(att_5_ip))
        return att_5_ip

    def Atten_6_ip_get(self):
        att_6_ip = self.conf.get("atten_config", "att_6_ip")
        logging.info("atten 6 ip is     : {0}".format(att_6_ip))
        return att_6_ip

    def Atten_7_ip_get(self):
        att_7_ip = self.conf.get("atten_config", "att_7_ip")
        logging.info("atten 7 ip is     : {0}".format(att_7_ip))
        return att_7_ip

    def Atten_8_ip_get(self):
        att_8_ip = self.conf.get("atten_config", "att_8_ip")
        logging.info("atten 8 ip is     : {0}".format(att_8_ip))
        return att_8_ip

    def dura_time_get(self):
        dura_time = self.conf.get("chariot_config", "duration")
        logging.info("dura_time is     : {0}".format(dura_time))
        return dura_time

    def pc_ip_get(self):
        pc_ip = self.conf.get("chariot_config", "pc_ip")
        logging.info("sta ip is     : {0}".format(pc_ip))
        return pc_ip

    def Sta_ip_get(self):
        sta_ip = self.conf.get("chariot_config", "sta_ip")
        logging.info("sta ip is     : {0}".format(sta_ip))
        return sta_ip

    def Dura_time_get(self):
        dura_time = self.conf.get("chariot_config", "duration")
        # logging.info("duration time is    : {0}".format(dura_time))
        return dura_time

    def Curr_att_get(self):
        curr_att = self.conf.get("chariot_config", "atten_value")
        logging.info("current attention is    : {0}".format(curr_att))
        return curr_att

    def angle_num_get(self):
        angle_num = self.conf.get("swivel_table_config", "angle_num")
        logging.info(" Degree is     : {0}".format(angle_num))
        return angle_num

    def current_angle_get(self):
        current_angle = self.conf.get("swivel_table_config", "current_angle")
        logging.info(" Current_angle is     : {0}".format(current_angle))
        return current_angle

    def table_com_get(self):
        com = self.conf.get("swivel_table_config", "com")
        logging.info(" Table COM is     : {0}".format(com))
        return com

    def Sta_type_get(self):
        sta_type = self.conf.get("sta_config", "sta_type")
        logging.info("sta ip is     : {0}".format(sta_type))
        return sta_type

    def Sta_address(self):
        sta_address = self.conf.get("sta_config", "sta_address")
        logging.info("sta address is     : {0}".format(sta_address))
        return sta_address

    def Sta_username(self):
        sta_username = self.conf.get("sta_config", "sta_username")
        logging.info("sta username is     : {0}".format(sta_username))
        return sta_username

    def Sta_password(self):
        sta_password = self.conf.get("sta_config", "sta_password")
        logging.info("sta password is     : {0}".format(sta_password))
        return sta_password

    def Run_type_get(self):
        run_type = self.conf.get("test_config", "test_type")
        # logging.info("duration time is    : {0}".format(dura_time))
        return run_type


# AP配置参数写入
class Dut_config(object):
    def __init__(self, aptype, dutip, username, password, radio, channel):
        self.aptype = aptype
        self.dutip = dutip
        self.username = username
        self.password = password
        self.radio = radio
        self.channel = channel
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Ap_config_set(self):
        self.conf.set("ap_config", "aptype", str(self.aptype))
        self.conf.set("ap_config", "dutip", str(self.dutip))
        self.conf.set("ap_config", "username", str(self.username))
        self.conf.set("ap_config", "password", str(self.password))
        self.conf.set("ap_config", "radio", str(self.radio))
        self.conf.set("ap_config", "channel", str(self.channel))
        self.conf.write(open(config_file, "w"))


# 衰减配置写入
class Atten_config(object):
    def __init__(self, start, end, step, loss, num):
        self.atten_start = start
        self.atten_end = end
        self.atten_step = step
        self.line_loss = loss
        self.atten_num = num
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Atten_config_set(self):
        self.conf.set("atten_config", "atten_start", str(self.atten_start))
        self.conf.set("atten_config", "atten_end", str(self.atten_end))
        self.conf.set("atten_config", "atten_step", str(self.atten_step))
        self.conf.set("atten_config", "line_loss", str(self.line_loss))
        self.conf.set("atten_config", "atten_num", str(self.atten_num))
        self.conf.write(open(config_file, "w"))


# chariot配置写入
class Chariot_config(object):
    def __init__(self, pcip, staip, duration, pairnumber):
        self.pcip = pcip
        self.staip = staip
        self.duration = duration
        self.pairnumber = pairnumber
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def chariot_set(self):
        self.conf.set("chariot_config", "pc_ip", str(self.pcip))
        self.conf.set("chariot_config", "sta_ip", str(self.staip))
        self.conf.set("chariot_config", "duration", str(self.duration))
        self.conf.set("chariot_config", "pairnumber", str(self.pairnumber))
        self.conf.write(open(config_file, "w"))


# 写配置，以便生成以当前衰减和角度命名的报告
class Con_current_atten:
    def __init__(self, atten):
        self.atten = atten
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def read_atten(self):
        current_atten = self.conf.get("chariot_config", "atten_value")
        logging.info("now the attention is   : {0}".format(current_atten))
        return current_atten

    def write_atten(self):
        self.conf.set("chariot_config", "atten_value", str(self.atten))
        self.conf.write(open(config_file, "w"))


# 写配置，以便生成以当前衰减和角度命名的报告
class Con_current_angle:
    def __init__(self, angle):
        self.angle = angle
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def read_current_angle(self):
        print('111', self.angle)
        angle = self.conf.get("swivel_table_config", "current_angle")
        print('222', angle)
        logging.info("now the angle is   : {0}".format(angle))
        return angle

    def write_angle(self):
        self.conf.set("swivel_table_config", "current_angle", str(self.angle))
        self.conf.write(open(config_file, "w"))


# 圆盘电机角度配置写入
class Swivel_table_config(object):
    def __init__(self, angle):
        self.angle = angle
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def swivel_table_type_set(self):
        self.conf.set("swivel_table_config", "angle", str(self.angle))
        self.conf.write(open(config_file, "w"))


# 终端类型配置写入
class Sta_config(object):
    def __init__(self, statype):
        self.sta_type = statype
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Sta_type_set(self):
        self.conf.set("sta_config", "sta_type", str(self.sta_type))
        self.conf.write(open(config_file, "w"))


# 测试类型写入
class Run_type_config(object):
    def __init__(self, runtype):
        self.run_type = runtype
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Run_type_set(self):
        self.conf.set("test_config", "test_type", str(self.run_type))
        self.conf.write(open(config_file, "w"))


conf = Config()

if __name__ == "__main__":
    #pass##
    ##dut_conf=Dut_config("WF-1821","192.168.188.251","admin","password","2","6")
    ##dut_conf.Ap_config_set()
    ##chariot=Chariot_config("192.168.1.10","192.168.1.20",90,8,10)
    ##chariot.chariot_set()
    get = Config()
    ip = get.Atten_1_ip_get()
    print(ip)
    print(get)
    for i in {10, 20}:
        x = 20
        att = Con_current_atten(20)
        value = att.read_atten()
        print(value)

        att.write_atten()
        value = att.read_atten()
        print(value)

    for i in {10, 20}:
        x = 20
        angle = Con_current_angle(90)
        value = angle.read_current_angle()
        print(value)

        angle.write_angle()
        value = angle.read_current_angle()
        print(value)



    #atten.Atten_config_set()
    #staconfig=Sta_config("WF-2821")
    #staconfig.Sta_type_set()"""
