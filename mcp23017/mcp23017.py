#!/usr/bin/python
#-*- encoding: utf-8 -*-
from periphery import I2C

class mcp23017:
	def __init__(self, device, addr): 
		self.i2c = I2C(device)
		self.i2c_addr = addr
			
		self.act_ioA = 0x00
		self.act_ioB = 0x00
		self.act_pinA = 0x00
		self.act_pinB = 0x00

		self.IODIRB = 0x01 # Pin direction register
		self.IODIRA = 0x00 # Pin direction register
		self.OLATA = 0x14 # Register for outputs
		self.OLATB = 0x15 # Register for outputs
		self.GPIOA = 0x12 # Register for inputs
		self.GPIOB = 0x13 # Register for inputs

	def setup(self, pin, io, side):
	# setup( 0, 'OUT', 'A')
	# pin (0,7)  io (IN,OUT)  side (A,B)

		if (pin<0 or pin>7) or (side!='A' and side!='B') or (io!='IN' and io!='OUT'):
			print(' --- setup(pin, io, side) ---')
			print(' --- pin (0 - 7)  io (IN or OUT)  side (A or B) ---')
			return;
	
		if io=='IN' and side=='A':
			pinio = self.act_ioA | (1<<pin)
			self.act_ioA=pinio
		elif io=='OUT' and side=='A':
			pinio = self.act_ioA & ~(1<<pin)
			self.act_ioA=pinio
		elif io=='IN' and side=='B':
			pinio = self.act_ioB | (1<<pin)
			self.act_ioB=pinio
		elif io=='OUT' and side=='B':
			pinio = self.act_ioB & ~(1<<pin)
			self.act_ioB=pinio
		else:
			retrun
		
		try:
			if side=='A':
				msgs = [I2C.Message([self.IODIRA]), I2C.Message([pinio], read=False)]
				self.i2c.transfer(self.i2c_addr, msgs)
			else:
				msgs = [I2C.Message([self.IODIRB]), I2C.Message([pinio], read=False)]
				self.i2c.transfer(self.i2c_addr, msgs)
	
			return;

		except:
			print(' --- Error accessing the chip MCP23017 ---')
			raise
	
	def output(self, pin, hl, side):
	# output(0, 1, 'A') 
	# pin (0,7)  hl (0,1)  side (A,B)
	
		if (pin<0 or pin>7) or (side!='A' and side!='B') or (hl!=1 and hl!=0):
			print(' --- output(pin, hl, side) ---')
			print(' --- pin (0 - 7)  hl (0 or 1)  side (A or B) ---')
			return;

		if hl==1 and side=='A':
			pinhl = self.act_pinA | (1<<pin)
			self.act_pinA=pinhl
		elif hl==0 and side=='A':
			pinhl = self.act_pinA & ~(1<<pin)
			self.act_pinA=pinhl
		elif hl==1 and side=='B':
			pinhl = self.act_pinB | (1<<pin)
			self.act_pinB=pinhl
		elif hl==0 and side=='B':
			pinhl = self.act_pinB & ~(1<<pin)
			self.act_pinB=pinhl
		else:
			return

		try:
			if side=='A':
				#print("pinhl={:x}".format(pinhl))
				msgs = [I2C.Message([self.OLATA]), I2C.Message([pinhl], read=False)]
				self.i2c.transfer(self.i2c_addr, msgs)
			else:
				#print("pinhl={:x}".format(pinhl))
				msgs = [I2C.Message([self.OLATB]), I2C.Message([pinhl], read=False)]
				self.i2c.transfer(self.i2c_addr, msgs)
	
			return;
		
		except:
			print(' --- Error accessing the chip MCP23017 ---')
			raise
	
	def input(self, pin, side):
	# input(7, 'B', port_expander)
	# pin (0,7)  side (A,B)
		if (pin<0 or pin>7) or (side!='A' and side!='B'):
			print(' --- MySwitch = GPIO.input(pin, side) ---')
			print(' --- pin (0 - 7)  side (A or B) ---')
			return;

		try:
			if side=='A':
				msgs = [I2C.Message([self.GPIOA]), I2C.Message([0], read=True)]
				self.i2c.transfer(self.i2c_addr, msgs)
				MySwitch = msgs[1].data[0]
				if MySwitch & (1<<pin) == (1<<pin):
					MySwitch=1
				else:
					MySwitch=0
			else:
				msgs = [I2C.Message([self.GPIOB]), I2C.Message([0], read=True)]
				self.i2c.transfer(self.i2c_addr, msgs)
				MySwitch = msgs[1].data[0]
				if MySwitch & (1<<pin) == (1<<pin):
					MySwitch=1
				else:
					MySwitch=0
	  
			return MySwitch;
		except:
			print(' --- Error accessing the chip MCP23017 ---')
			raise
