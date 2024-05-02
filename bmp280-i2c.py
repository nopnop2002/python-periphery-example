#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import time
import signal
from ctypes import c_short
from ctypes import c_int
import argparse
from periphery import I2C

i2c = None
ic2_addr = 0
DEBUG = 0

def handler(signal, frame):
    global running
    print('handler')
    running = False

def getShort(data, index):
	# return two bytes from data as a signed 16-bit value
	return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
	# return two bytes from data as an unsigned 16-bit value
	return (data[index+1] << 8) + data[index]

def getChar(data,index):
	# return one byte from data as a signed char
	result = data[index]
	if result > 127:
		result -= 256
	return result

def getUChar(data,index):
	# return one byte from data as an unsigned char
	result = data[index] & 0xFF
	return result

def readID(addr=ic2_addr):
	# Chip ID Register Address
	REG_ID = 0xD0
	msgs = [I2C.Message([REG_ID]), I2C.Message([0,0], read=True)]
	i2c.transfer(ic2_addr, msgs)
	chip_id = msgs[1].data[0]
	chip_version = msgs[1].data[1]
	return chip_id, chip_version

def readBME280All(addr=ic2_addr):
	# Register Addresses
	REG_DATA = 0xF7
	REG_CONTROL = 0xF4
	REG_CONFIG	= 0xF5

	REG_CONTROL_HUM = 0xF2
	REG_HUM_MSB = 0xFD
	REG_HUM_LSB = 0xFE

	# Oversample setting - page 27
	OVERSAMPLE_TEMP = 2
	OVERSAMPLE_PRES = 2
	MODE = 1

	# Oversample setting for humidity register - page 26
	OVERSAMPLE_HUM = 2
	msgs = [I2C.Message([REG_CONTROL_HUM, OVERSAMPLE_HUM]), I2C.Message([0], read=False)]
	i2c.transfer(ic2_addr, msgs)

	control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
	msgs = [I2C.Message([REG_CONTROL, control]), I2C.Message([0], read=False)]
	i2c.transfer(ic2_addr, msgs)

	# Read blocks of calibration data from EEPROM
	# See Page 22 data sheet
	cal1 = [0 for i in range(24)]
	msgs = [I2C.Message([0x88]), I2C.Message(cal1, read=True)]
	i2c.transfer(ic2_addr, msgs)
	cal1 = []
	for x in range(24):
		cal1.append(msgs[1].data[x])

	cal2 = []
	msgs = [I2C.Message([0xA1]), I2C.Message([0], read=True)]
	i2c.transfer(ic2_addr, msgs)
	cal2.append(msgs[1].data[0])

	cal3 = [0 for i in range(7)]
	msgs = [I2C.Message([0xE1]), I2C.Message(cal3, read=True)]
	i2c.transfer(ic2_addr, msgs)
	cal3 = []
	for x in range(7):
		cal3.append(msgs[1].data[x])

	# Convert byte data to word values
	dig_T1 = getUShort(cal1, 0)
	dig_T2 = getShort(cal1, 2)
	dig_T3 = getShort(cal1, 4)
	if(DEBUG == 1):
		print("dig_T1 = %d" % dig_T1),
		print("dig_T2 = %d" % dig_T2),
		print("dig_T3 = %d" % dig_T3)

	dig_P1 = getUShort(cal1, 6)
	dig_P2 = getShort(cal1, 8)
	dig_P3 = getShort(cal1, 10)
	dig_P4 = getShort(cal1, 12)
	dig_P5 = getShort(cal1, 14)
	dig_P6 = getShort(cal1, 16)
	dig_P7 = getShort(cal1, 18)
	dig_P8 = getShort(cal1, 20)
	dig_P9 = getShort(cal1, 22)

	dig_H1 = getUChar(cal2, 0)
	dig_H2 = getShort(cal3, 0)
	dig_H3 = getUChar(cal3, 2)

	dig_H4 = getChar(cal3, 3)
	dig_H4 = (dig_H4 << 24) >> 20
	dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

	dig_H5 = getChar(cal3, 5)
	dig_H5 = (dig_H5 << 24) >> 20
	dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

	dig_H6 = getChar(cal3, 6)

	# Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
	wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
	time.sleep(wait_time/1000)	# Wait the required time

	# Read temperature/pressure/humidity
	data = [0 for i in range(8)]
	msgs = [I2C.Message([REG_DATA]), I2C.Message(data, read=True)]
	i2c.transfer(ic2_addr, msgs)
	data = []
	for x in range(8):
		data.append(msgs[1].data[x])
	pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
	temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
	hum_raw = (data[6] << 8) | data[7]

	#Refine temperature
	var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
	var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
	t_fine = c_int(var1 + var2).value
	temperature = float(((t_fine * 5) + 128) >> 8);

	# Refine pressure and adjust for temperature
	var1 = t_fine / 2.0 - 64000.0
	var2 = var1 * var1 * dig_P6 / 32768.0
	var2 = var2 + var1 * dig_P5 * 2.0
	var2 = var2 / 4.0 + dig_P4 * 65536.0
	var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
	var1 = (1.0 + var1 / 32768.0) * dig_P1
	if var1 == 0:
		pressure=0
	else:
		pressure = 1048576.0 - pres_raw
		pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
		var1 = dig_P9 * pressure * pressure / 2147483648.0
		var2 = pressure * dig_P8 / 32768.0
		pressure = pressure + (var1 + var2 + dig_P7) / 16.0

	# Refine humidity
	humidity = t_fine - 76800.0
	humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
	humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
	if humidity > 100:
		humidity = 100
	elif humidity < 0:
		humidity = 0

	return temperature/100.0,pressure/100.0,humidity

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help="device file name", default='/dev/i2c-0')
	parser.add_argument('-a', '--addr', type=lambda x: int(x, 16), help="i2c address", default=0x76)
	parser.add_argument('-p', '--print', type=int, help="print debug", default=0)
	args = parser.parse_args()

	# Open i2c device
	print("device={}".format(args.device))
	print("addr=0x{:x}".format(args.addr))
	i2c = I2C(args.device)
	ic2_addr = args.addr
	DEBUG = args.print

	chip_id, chip_version = readID()
	print("chip_id = 0x{:x} ".format(chip_id), end="")
	if (chip_id == 0x58):
		print("BMP280")
	elif (chip_id == 0x60):
		print("BME280")
	else:
		print("Unknown")
		sys.exit()

	while running:
		print("-----------------------")

		print("Chip ID     : 0x{:x}".format(chip_id))
		if (chip_id == 0x60):
			print("Version    :{}".format(chip_version))

		temperature,pressure,humidity = readBME280All()

		print("Temperature : {:.2f} C".format(temperature))
		print("Pressure    : {:.2f} hPa".format(pressure))
		if (chip_id == 0x60):
			print("Humidity	     : {:.2f} %".format(humidity))
		time.sleep(2)
