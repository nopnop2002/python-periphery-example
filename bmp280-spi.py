#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import time
import signal
import argparse
from ctypes import c_short
from ctypes import c_int
from periphery import SPI

spi = None
DEBUG = 0

def handler(signal, frame):
    global running
    print('handler')
    running = False

def readID():
	out = [0xD0, 0x00, 0x00]
	resp = spi.transfer(out)
	if(DEBUG == 1):print("resp = {}".format(resp))
	return resp[1], resp[2]

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

def readData():
	while(1):
		out = []
		for x in range(0xF7, 0xFD):
			out.append(x)
		out.append(0)
		resp = spi.transfer(out)
		if(DEBUG == 1): print(resp)
		# Check valid data
		if (resp[2] != 0 or resp[3] != 0):break
		time.sleep(1)

	pres_raw = (resp[1] << 12) | (resp[2] << 4) | (resp[3] >> 4)	#0xF7, msb+lsb+xlsb=19bit
	if(DEBUG == 1):print("pres_raw = %d " % pres_raw)
	temp_raw = (resp[4] << 12) | (resp[5] << 4) | (resp[6] >> 4)	#0xFA, msb+lsb+xlsb=19bit
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
	parser.add_argument('-d', '--device', help="device file name", default='/dev/spidev0.0')
	parser.add_argument('-m', '--mode', type=int, help="spi mode", default=0)
	parser.add_argument('-s', '--speed', type=int, help="spi clock speed", default=1000000)
	parser.add_argument('-p', '--print', type=int, help="print debug", default=0)
	args = parser.parse_args()

	# Open spi device
	print("device={}".format(args.device))
	print("mode={}".format(args.mode))
	print("speed={}".format(args.speed))
	print("print={}".format(args.print))
	#spi = SPI(args.device, 0, 1000000)
	spi = SPI(args.device, args.mode, args.speed)
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

	t_sb = 5    #stanby 1000ms
	filter = 0	#filter O = off
	spi3or4 = 0 #SPI 3wire or 4wire, 0=4wire, 1=3wire
	osrs_t = 4	#OverSampling Temperature x8
	osrs_p = 4	#OverSampling Pressure x8
	Mode = 3    #Normal mode

	temp_raw = 0
	pres_raw = 0
	t_fine = 0

	# Send a command to the control register[0xF4]
	ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | Mode
	if(DEBUG == 1):print("ctrl_meas_reg = %x" % ctrl_meas_reg)
	spi.transfer([0x74,ctrl_meas_reg])

	# Send a command to the config register[0xF5]
	config_reg = (t_sb << 5) | (filter << 2) | spi3or4
	if(DEBUG == 1):print("config_reg = %x " % config_reg)
	spi.transfer([0x75,config_reg])

	# Check control[0xF4] & config register[0xF5]
	print('Check Register')
	out = [0xF4, 0xF5, 0x00]
	resp = spi.transfer(out)
	if(DEBUG == 1):
		print(resp)
		print("ctrl_meas_reg = %x" % resp[1])
		print("config_reg		 = %x" % resp[2])
	if(resp[1] != ctrl_meas_reg):
		print("INVALID control register %x" % resp[1])
	if(resp[2] != config_reg):
		print("INVALID config  register %x" % resp[2])

	print('Read calibration data')
	a = []
	for x in range(0x88, 0xA0):
		a.append(x)
	a.append(0)
	resp = spi.transfer(a)
	if(DEBUG == 1): print(resp)

	dig_T1 = resp[2] * 256 + resp[1]
	dig_T2 = c_short(resp[4] * 256 + resp[3]).value
	dig_T3 = c_short(resp[6] * 256 + resp[5]).value
	if(DEBUG == 1):
		print("dig_T1 = %d" % dig_T1),
		print("dig_T2 = %d" % dig_T2),
		print("dig_T3 = %d" % dig_T3)

	dig_P1 = resp[8] * 256 + resp[7]
	dig_P2 = c_short(resp[10] * 256 + resp[9]).value
	dig_P3 = c_short(resp[12] * 256 + resp[11]).value
	dig_P4 = c_short(resp[14] * 256 + resp[13]).value
	dig_P5 = c_short(resp[16] * 256 + resp[15]).value
	dig_P6 = c_short(resp[18] * 256 + resp[17]).value
	dig_P7 = c_short(resp[20] * 256 + resp[19]).value
	dig_P8 = c_short(resp[22] * 256 + resp[21]).value
	dig_P9 = c_short(resp[24] * 256 + resp[23]).value
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
		print("-----------------------")
		print("Chip ID     : 0x{:x}".format(chip_id))
		print("Temperature : {} C".format(temp_act))
		print("Pressure    : {} hPa".format(press_act))
		time.sleep(2)
