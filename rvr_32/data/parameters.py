__author__ = 'DVTRF'

from config import conf

""""
主要是配置參數
"""
# ap参数
AP_TYPE = str(conf.Ap_type_get()).strip()
HOST_IP = str(conf.Dutip_get()).strip()
USER_NAME = str(conf.Username_get()).strip()
PASSWORD = str(conf.Password_get()).strip()
SSID = str(conf.SSID_get()).strip()
RADIO = str(conf.Radio_get()).strip()
CHANNEL = str(conf.Channel_get()).strip()
AP_COM = str(conf.COM_get()).strip()
AP_BAUDRATE = str(conf.Baudrate_get()).strip()

# station parameters
STA_TYPE = str(conf.Sta_type_get()).strip()
STA_ADDRESS = str(conf.Sta_address()).strip()
STA_USERNAME = str(conf.Sta_username()).strip()
STA_PASSWORD = str(conf.Sta_password()).strip()
STA_SWITCHIP = str(conf.Sta_switchip_get()).strip()
STA_SWITCHPORT = str(conf.Sta_switchport_get()).strip()

# 衰减参数
ATTEN_START = int(conf.Atten_start_get())
ATTEN_END = int(conf.Atten_end_get())
ATTEN_STEP = int(conf.Atten_step_get())
LINE_LOSS = int(conf.External_loss_get())
CURRENT_ATT = int(conf.Curr_att_get())
ATTEN_NUM: int = int(conf.Atten_num_get())
assert ATTEN_NUM > 0
ATTENUATE_LIST = []
ATT = ATTEN_START
while ATT <= ATTEN_END:
    ATTENUATE_LIST.append(ATT)
    ATT = ATT + ATTEN_STEP

# chariot参数
DURA_TIME = int(conf.dura_time_get())

# 转动角度参数
ANGLE_NUM = int(conf.angle_num_get())
angle_setup = 360.0 / float(ANGLE_NUM)
angle = 0
ANGLE_LIST = []
while angle < 360.0:
    ANGLE_LIST.append(angle)
    angle += angle_setup
TABLE_COM = str(conf.table_com_get()).strip()

# STA参数


# TESTTYPE参数
RUN_TPYE = int(conf.Run_type_get())
