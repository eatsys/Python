#encoding: Utf-8
import sys
import socket
import datetime
import time
import telnetlib
#import serial
from datetime import date
 
try:
	tn = telnetlib.Telnet('192.168.1.1')
	tn.set_debuglevel(1)
	#print tn.host
	tn.read_until("root@OpenWrt:/#")
	n = tn.write(b"/etc/init.d/art start" + "\r")
	print n
	tn.read_until("root@OpenWrt:/#")
	tn.close()
finally:
	time.sleep(5)
