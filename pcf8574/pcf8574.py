#!/usr/bin/python
#-*- encoding: utf-8 -*-
from periphery import I2C

class pcf8574:
	def __init__(self, device, addr, print=False):
		self.i2c = I2C(device)
		self.i2c_addr = addr
		self.print = print
		try:
			msgs = [I2C.Message([0x00], read=False)]
			self.i2c.transfer(self.i2c_addr, msgs)
		except Exception as ex:
			print(ex)
			return

	def set_pin(self, pin_num, status):
		try:
			msgs = [I2C.Message([0x00], read=True)]
			self.i2c.transfer(self.i2c_addr, msgs)
			value = msgs[0].data[0]
			if (self.print): print("value=0x{:x}".format(value))
			if (status):
				value = value | (1<<pin_num)
			else:
				value = value & ~(1<<pin_num)
			if (self.print): print("value=0x{:x}".format(value))
			msgs = [I2C.Message([value], read=False)]
			self.i2c.transfer(self.i2c_addr, msgs)
		except Exception as ex:
			print(ex)
			return

	def get_pin(self, pin_num):
		try:
			msgs = [I2C.Message([0x00], read=True)]
			self.i2c.transfer(self.i2c_addr, msgs)
			value = msgs[0].data[0]
			if (self.print): print("value=0x{:x}".format(value))
			value = value & (1<<pin_num)
			if value: return 1
			else: return 0
		except Exception as ex:
			print(ex)
			return

	def get_value(self):
		try:
			msgs = [I2C.Message([0x00], read=True)]
			self.i2c.transfer(self.i2c_addr, msgs)
			value = msgs[0].data[0]
			return value
		except Exception as ex:
			print(ex)
			return
