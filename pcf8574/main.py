#!/usr/bin/python
#-*- encoding: utf-8 -*-
import argparse
import time
from pcf8574 import pcf8574

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help="device file name", default='/dev/i2c-1')
	parser.add_argument('-a', '--addr', type=lambda x: int(x, 16), help="i2c address", default=0x20)	
	parser.add_argument('--delay', type=float, help="Delay time", default=0.1)	
	args = parser.parse_args()	

	pcf = pcf8574(args.device, args.addr)
	print("value=0x{:x}".format(pcf.get_value()))

	for i in range(8):
		pcf.set_pin(i, True)
		print("value=0x{:x}".format(pcf.get_value()))
		time.sleep(args.delay)

	time.sleep(1)
	for i in range(8):
		pcf.set_pin(7-i, False)
		print("value=0x{:x}".format(pcf.get_value()))
		time.sleep(args.delay)
