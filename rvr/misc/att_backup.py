# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan
# @FileName: pdv.py

#import win32com.client
#from ctypes import *
#import pythoncom
#import datetime
#import time
#import os
## import numpy
## from numpy import *
##att = win32com.client.Dispatch("C:\Program Files (x86)\Mini-Circuits Programmable Attenuator\mcl_RUDAT.exe")
#att = CDLL('mcl_RUDAT64.dll')
#print(att)
#cn = att.connect()
#print(cn)
#Attenuation = 0.0
#cn = att.Read_Att(Attenuation)
#print(cn)
#cn = att.SetAttenuation(37)
#cn = att.Read_Att(Attenuation)
#print(cn)
#att.Disconnect

#mport subprocess
#rom subprocess import Popen, PIPE
# Define a function to use the executable and return the response
#ef Command_Attenuator():
#   sn = '11602280075' # Serial number of the attenuator to control
#   # Call the executable, passing the serial number and SCPI commands as arguments
#   pipe = subprocess.Popen('mcl_RUDAT.exe -sn ' + sn, stdout=subprocess.PIPE)
#   pipe.wait
#   Attenuator_Response = pipe.stdout.read()
#   ##eturn Attenuator_Response
#   # Use the above function to send any SCPI commands to the attenuator
#   # Refer to programming manual section 5.4 for full list of SCPI commands
#   ModelName = Command_Attenuator(":MN?") # Read model name
#   print(ModelName)
#   SerialNo = Command_Attenuator(":SN?") # Read serial number
#   print(SerialNo)
#   Command_Attenuator(":SETATT=12.75") # Set attenuation
#   Att = Command_Attenuator(":ATT?") # Read attenuation
#   print(Att)
#   Command_Attenuator(":SETATT=25") # Set attenuation
#   Att = Command_Attenuator(":ATT?") # Read attenuation
#   print(Att)
##f __name__ == '__main__':
#   Command_Attenuator()


#from win32com.client import Dispatch
#import pythoncom
#import datetime
#import time
#import os
#import numpy
#from numpy import *
##att = Dispatch("mcl_RUDAT.Application")
#att = win32com.client.DispatchEx("mcl_RUDAT.USB_DAT")
#att = pythoncom.LoadRegTypeLib("mcl_RUDAT.USB_DAT")
#att = win32com.client.DispatchEx("mcl_RUDAT.exe")
#print(att)
#print(att.Ver())
#cn = att.Connect()
#Attenuation = 0.0
#cn = att.Read_Att(Attenuation)
#print(cn)
#cn = att.SetAttenuation(37)
#cn = att.Read_Att(Attenuation)
#print(cn)
#att.Disconnect

import comtypes
from comtypes.client import CreateObject

att = CreateObject("mcl_RUDAT")
version = att.GetVersion()
print(version)
Attenuation = 0.0
cn = att.Connect()
cn = att.Read_Att(Attenuation)
print(cn)

