#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from periphery import I2C
import argparse

def scan(address):
	try:
		msgs = [I2C.Message([0x00]), I2C.Message([0,0], read=True)]
		i2c.transfer(address, msgs)
		print('{:x} '.format(address), end="")
	except: # exception if read_byte fails
		print('-- ', end="")

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', default='/dev/i2c-0')
	args = parser.parse_args()

	print("device={}".format(args.device))
	i2c = I2C(args.device)

	print('   ', end="")
	for index in range(16):
		print('  {:x}'.format(index), end="")
	print()

	print('00:          ', end="")
	for device in range(3,16):
		scan(device)
	for index in range(1,7):
		start = index*16
		end   = (index+1)*16
		print('\n{:x}: '.format(start), end="")
		for device in range(start,end):
	   		scan(device)
	print('\n70: ', end="")
	for device in range(0x70,0x78):
		scan(device)
	print()
