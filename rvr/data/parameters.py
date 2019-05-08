__author__ = 'DVTRF'

#import config
#
#conf = config.Config()
from config import conf

""""
主要是配置參數
"""
# ap参数
AP_TYPE = conf.Ap_type_get()
HOST_IP = conf.Dutip_get()
USER_NAME = conf.Username_get()
PASSWORD = conf.Password_get()
SSID = conf.SSID_get()
RADIO = conf.Radio_get()
CHANNEL = conf.Channel_get()

# station parameters
STA_IP = conf.Sta_ip_get()

# 衰减参数
ATTEN_START = int(conf.Atten_start_get())
ATTEN_END = int(conf.Atten_end_get())
ATTEN_STEP = int(conf.Atten_step_get())
LINE_LOSS = int(conf.External_loss_get())
CURRENT_ATT = int(conf.Curr_att_get())
ATTEN_NUM = int(conf.Atten_num_get())
ATTENUATE_LIST = []
ATT = ATTEN_START
while ATT <= ATTEN_END:
    ATTENUATE_LIST.append(ATT)
    ATT = ATT + ATTEN_STEP

# chariot参数
DURA_TIME = int(conf.dura_time_get())

# 转动角度参数
ANGLE = int(conf.angle_num_get())

# STA参数
STA_IP = conf.Sta_ip_get()
STA_TYPE = conf.Sta_type_get()

# TESTTYPE参数
RUN_TPYE = int(conf.Run_type_get())
