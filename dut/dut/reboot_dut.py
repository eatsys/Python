#encoding: Utf-8
import sys
import os
import time
import telnetlib
 
try:
	ip = '192.168.1.1'
	tn = telnetlib.Telnet(ip)
	tn.set_debuglevel(1)
	print tn.host
	tn.read_until('root@OpenWrt:/# ')
	time.sleep(1)
	n = tn.write('ps\n')
	print n
	tn.read_until('root@OpenWrt:/# ')
	n = tn.write(b'reboot\n')
	print n
	ping_return = os.system('ping -n 3 -w 1 %s' % ip)
	print(ping_return)
	if ping_return == 0:
		print 'reboot ok'
		tn.close()
		time.sleep(60)
	else:
		tn.read_until('root@OpenWrt:/# ')
		n = tn.write(b'reboot\n')
		print n
		print 'reboot again'
		tn.close()
finally:
	time.sleep(1)
