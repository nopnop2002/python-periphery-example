#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import time
import signal
import argparse
from ctypes import c_short
from ctypes import c_int
from periphery import GPIO

def handler(signal, frame):
	global running
	print('handler')
	running = False

def calibration_T(adc_T):
	global t_fine
	var1 = ((((adc_T >> 3) - (dig_T1<<1))) * (dig_T2)) >> 11
	var2 = (((((adc_T >> 4) - (dig_T1)) * ((adc_T>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14

	t_fine = c_int(var1 + var2).value
	T = (t_fine * 5 + 128) >> 8
	return T

def calibration_P(adc_P):
	var1 = ((t_fine)>>1) - 64000
	if(DEBUG == 1):print("var1(1) = {}".format(var1))
	var2 = (((var1>>2) * (var1>>2)) >> 11) * (dig_P6)
	if(DEBUG == 1):print("var2(2) = {}".format(var2))
	var2 = var2 + ((var1*(dig_P5))<<1)
	if(DEBUG == 1):print("var2(3) = {}".format(var2))
	var2 = (var2>>2)+((dig_P4)<<16)
	if(DEBUG == 1):print("var2(4) = {}".format(var2))
	var1 = (((dig_P3 * (((var1>>2)*(var1>>2)) >> 13)) >>3) + (((dig_P2) * var1)>>1))>>18
	if(DEBUG == 1):print("var1(5) = {}".format(var1))
	var1 = ((((32768+var1))*(dig_P1))>>15)
	if(DEBUG == 1):print("var1(6) = {}".format(var1))
	if (var1 == 0):
		return 0
	P = ((((1048576)-adc_P)-(var2>>12)))*3125
	if(DEBUG == 1):print("P(7) = {} {}".format(type(P), P))
	if(P<0x80000000):
		P = int((P << 1) / (var1))
	if(P>=0x80000000):
		P = (P / var1) * 2;
	if(DEBUG == 1):print("P(8) = {} {}".format(type(P), P))
	var1 = ((dig_P9) * ((((P>>3) * (P>>3))>>13)))>>12
	var2 = (((P>>2)) * (dig_P8))>>13
	if(DEBUG == 1):
		print("var1 = {}".format(var1))
		print("var2 = {}".format(var2))
	P = (P + ((var1 + var2 + dig_P7) >> 4))
	if(DEBUG == 1):print("P = {} {}".format(type(P), P))
	return P

def writeReg(reg_address, data):
	gpio_cs.write(False)
	SoftSpiWrite(reg_address & 0x7F)	# write, bit 7 low
	SoftSpiWrite(data)
	gpio_cs.write(True)

def read16bit(reg):
	gpio_cs.write(False)
	SoftSpiWrite(reg | 0x80)	# read, bit 7 high
	d1 = SoftSpiRead()
	d2 = SoftSpiRead()
	data = (d2 << 8) | d1
	gpio_cs.write(True)
	return data

def read8bit(reg):
	gpio_cs.write(False)
	SoftSpiWrite(reg | 0x80)	# read, bit 7 high
	data = SoftSpiRead();
	gpio_cs.write(True)
	return data;

def SoftSpiWrite(data):
	mask = 0x80
	for x in range(8):
		gpio_sclk.write(False)
		bit = data & mask
		if (bit != 0):
			gpio_mosi.write(True)
		if (bit == 0):
			gpio_mosi.write(False)
		gpio_sclk.write(True)
		mask = mask >> 1

def SoftSpiRead():
	r_data = 0;
	mask = 0x80
	gpio_mosi.write(False)
	for x in range(8):
		r_data = r_data << 1
		gpio_sclk.write(False)
		gpio_sclk.write(True)
		bit = gpio_miso.read()
		if (bit == True):
			r_data = r_data + 1
	return r_data;

def readData():
	while(1):
		resp = []
		register = 0xF7
		for x in range(6):
			 value = read8bit(register)
			 if(DEBUG == 1):print(value)
			 resp.append(value)
			 register=register+1
		if(DEBUG == 1):print
		# Check valid data
		if (resp[2] != 0 or resp[3] != 0):break
		time.sleep(1)

	pres_raw = (resp[0] << 12) | (resp[1] << 4) | (resp[2] >> 4)	#0xF7, msb+lsb+xlsb=19bit
	if(DEBUG == 1):print("pres_raw = %d " % pres_raw)
	temp_raw = (resp[3] << 12) | (resp[4] << 4) | (resp[5] >> 4)	#0xFA, msb+lsb+xlsb=19bit
	if(DEBUG == 1):print("temp_raw = %d " % temp_raw)

	temp_cal = calibration_T(temp_raw)
	if(DEBUG == 1):print("temp_cal = %d " % temp_cal)
	press_cal = calibration_P(pres_raw)
	if(DEBUG == 1):print("press_cal = %d " % press_cal)
	temp_act = temp_cal / 100.0
	press_act = press_cal / 100.0
	return temp_act, press_act

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('--sclk', type=int, help="spi sclk gpio", default=55)
	parser.add_argument('--mosi', type=int, help="spi mosi gpio", default=54)
	parser.add_argument('--cs', type=int, help="spi cs gpio", default=68)
	parser.add_argument('--miso', type=int, help="spi miso gpio", default=69)
	parser.add_argument('--print', type=int, help="print debug", default=0)
	args = parser.parse_args()

	# Set gpio direction
	print("sclk={}".format(args.sclk))
	print("mosi={}".format(args.mosi))
	print("cs={}".format(args.cs))
	print("miso={}".format(args.miso))
	print("print={}".format(args.print))
	gpio_mosi = GPIO(args.mosi, "out")
	gpio_miso = GPIO(args.miso, "in")
	gpio_sclk = GPIO(args.sclk, "out")
	gpio_cs = GPIO(args.cs, "out")
	DEBUG = args.print

	chip_id = read8bit(0xD0)
	print("chip_id = 0x{:x} ".format(chip_id), end="")
	if (chip_id == 0x58):
		print("BMP280")
	elif (chip_id == 0x60):
		print("BME280")
	else:
		print("Unknown")
		sys.exit()

	t_sb = 5	#stanby 1000ms
	filter = 0	#filter O = off
	spi3or4 = 0 #SPI 3wire or 4wire, 0=4wire, 1=3wire
	osrs_t = 4	#OverSampling Temperature x8
	osrs_p = 4	#OverSampling Pressure x8
	Mode = 3	#Normal mode

	temp_raw = 0
	pres_raw = 0
	t_fine = 0

	# Send a command to the control register[0xF4]
	ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | Mode
	if(DEBUG == 1):print("ctrl_meas_reg = %x" % ctrl_meas_reg)
	writeReg(0xF4,ctrl_meas_reg)

	# Send a command to the config register[0xF5]
	config_reg		= (t_sb << 5) | (filter << 2) | spi3or4
	if(DEBUG == 1):print("config_reg = %x " % config_reg)
	writeReg(0xF5,config_reg)

	print('Read calibration data')
	dig_T1 = read16bit(0x88)
	dig_T2 = c_short(read16bit(0x8A)).value
	dig_T3 = c_short(read16bit(0x8C)).value
	if(DEBUG == 1):
		print("dig_T1 = %d" % dig_T1),
		print("dig_T2 = %d" % dig_T2),
		print("dig_T3 = %d" % dig_T3)
	dig_P1 = read16bit(0x8E)
	dig_P2 = c_short(read16bit(0x90)).value
	dig_P3 = c_short(read16bit(0x92)).value
	dig_P4 = c_short(read16bit(0x94)).value
	dig_P5 = c_short(read16bit(0x96)).value
	dig_P6 = c_short(read16bit(0x98)).value
	dig_P7 = c_short(read16bit(0x9A)).value
	dig_P8 = c_short(read16bit(0x9C)).value
	dig_P9 = c_short(read16bit(0x9E)).value
	if(DEBUG == 1):
		print("dig_P1 = %d" % dig_P1),
		print("dig_P2 = %d" % dig_P2),
		print("dig_P3 = %d" % dig_P3)
		print("dig_P4 = %d" % dig_P4),
		print("dig_P5 = %d" % dig_P5),
		print("dig_P6 = %d" % dig_P6)
		print("dig_P7 = %d" % dig_P7),
		print("dig_P8 = %d" % dig_P8),
		print("dig_P9 = %d" % dig_P9)

	while running:
		temp_act, press_act = readData()
		print("-----------------------");
		print("Chip ID     : 0x{:x}".format(chip_id))
		print("Temperature : {} C".format(temp_act))
		print("Pressure    : {} hPa".format(press_act))
		time.sleep(2)
