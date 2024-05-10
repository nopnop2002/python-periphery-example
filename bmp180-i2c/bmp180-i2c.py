#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import time
import signal
from ctypes import c_short
import argparse
from periphery import I2C

def handler(signal, frame):
	global running
	print('handler')
	running = False

def getShort(data, index):
	# return two bytes from data as a signed 16-bit value
	return c_short((data[index] << 8) + data[index + 1]).value

def getUshort(data, index):
	# return two bytes from data as an unsigned 16-bit value
	return (data[index] << 8) + data[index + 1]

def readBmp180Id(addr):
	# Chip ID Register Address
	REG_ID		 = 0xD0
	msgs = [I2C.Message([REG_ID]), I2C.Message([0,0], read=True)]
	i2c.transfer(addr, msgs)
	chip_id = msgs[1].data[0]
	chip_version = msgs[1].data[1]
	return chip_id, chip_version

def readBmp180(addr):
	# Register Addresses
	REG_CALIB  = 0xAA
	REG_MEAS	 = 0xF4
	REG_MSB		 = 0xF6
	REG_LSB		 = 0xF7
	# Control Register Address
	CRV_TEMP	 = 0x2E
	CRV_PRES	 = 0x34
	# Oversample setting
	OVERSAMPLE = 3		# 0 - 3

	# Read calibration data
	# Read calibration data from EEPROM
	cal = [0 for i in range(22)]
	msgs = [I2C.Message([REG_CALIB]), I2C.Message(cal, read=True)]
	i2c.transfer(addr, msgs)
	cal = []
	for x in range(22):
		data = msgs[1].data[x]
		cal.append(data)

	# Convert byte data to word values
	AC1 = getShort(cal, 0)
	AC2 = getShort(cal, 2)
	AC3 = getShort(cal, 4)
	AC4 = getUshort(cal, 6)
	AC5 = getUshort(cal, 8)
	AC6 = getUshort(cal, 10)
	B1	= getShort(cal, 12)
	B2	= getShort(cal, 14)
	MB	= getShort(cal, 16)
	MC	= getShort(cal, 18)
	MD	= getShort(cal, 20)

	# Read temperature
	msgs = [I2C.Message([REG_MEAS,CRV_TEMP]), I2C.Message([0], read=False)]
	i2c.transfer(addr, msgs)
	time.sleep(0.005)
	msgs = [I2C.Message([REG_MSB]), I2C.Message([0,0], read=True)]
	i2c.transfer(addr, msgs)
	msb = msgs[1].data[0]
	lsb = msgs[1].data[1]
	UT = (msb << 8) + lsb

	# Read pressure
	msgs = [I2C.Message([REG_MEAS,CRV_PRES + (OVERSAMPLE << 6)]), I2C.Message([0], read=False)]
	i2c.transfer(addr, msgs)
	time.sleep(0.04)
	msgs = [I2C.Message([REG_MSB]), I2C.Message([0,0,0], read=True)]
	i2c.transfer(addr, msgs)
	msb = msgs[1].data[0]
	lsb = msgs[1].data[1]
	xsb = msgs[1].data[2]
	UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

	# Refine temperature
	X1 = ((UT - AC6) * AC5) >> 15
	X2 = (MC << 11) / (X1 + MD)
	B5 = X1 + X2
	temperature = int(B5 + 8) >> 4

	# Refine pressure
	B6	= B5 - 4000
	B62 = int(B6 * B6) >> 12
	X1	= (B2 * B62) >> 11
	X2	= int(AC2 * B6) >> 11
	X3	= X1 + X2
	B3	= (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

	X1 = int(AC3 * B6) >> 13
	X2 = (B1 * B62) >> 16
	X3 = ((X1 + X2) + 2) >> 2
	B4 = (AC4 * (X3 + 32768)) >> 15
	B7 = (UP - B3) * (50000 >> OVERSAMPLE)

	P = (B7 * 2) / B4

	X1 = (int(P) >> 8) * (int(P) >> 8)
	X1 = (X1 * 3038) >> 16
	X2 = int(-7357 * P) >> 16
	pressure = int(P + ((X1 + X2 + 3791) >> 4))

	return (temperature/10.0,pressure/100.0)

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help="device file name", default='/dev/i2c-1')
	parser.add_argument('-a', '--addr', type=lambda x: int(x, 16), help="i2c address", default=0x77)
	args = parser.parse_args()

	# Open i2c device
	print("device={}".format(args.device))
	print("addr=0x{:x}".format(args.addr))
	i2c = I2C(args.device)
	i2c_addr = args.addr

	chip_id, chip_version = readBmp180Id(i2c_addr)
	print("Chip ID		 : {0}".format(chip_id))
	print("Version		 : {0}".format(chip_version))
	print

	while running:
		print("-----------------------");
		print("Chip ID     : 0x{:x}".format(chip_id))
		(temperature,pressure)=readBmp180(i2c_addr)
		print("Temperature : {0} C".format(temperature))
		print("Pressure    : {0} hPa".format(pressure))
		time.sleep(2)

	i2c.close()

