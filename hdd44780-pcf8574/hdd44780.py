"""
python-periphery 1602 LCD sample

I ported from here
https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
"""
#!/usr/bin/python
#-*- encoding: utf-8 -*-
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pcf8574.pcf8574 import pcf8574

class hdd44780:
	def __init__(self, device, addr):	

		self.device = device
		self.addr = addr
		self.pcf = pcf8574(self.device, self.addr)

		self.LCD_RS = 0 # pin  4 on the PCF8574
		self.LCD_EN = 1 # pin  5 on the PCF8574
		self.LCD_D4 = 7 # pin  9 on the PCF8574
		self.LCD_D5 = 6 # pin 10 on the PCF8574
		self.LCD_D6 = 5 # pin 11 on the PCF8574
		self.LCD_D7 = 4 # pin 12 on the PCF8574

		self.pcf.set_pin(self.LCD_RS, False)
		self.pcf.set_pin(self.LCD_EN, False)
		self.pcf.set_pin(self.LCD_D4, False)
		self.pcf.set_pin(self.LCD_D5, False)
		self.pcf.set_pin(self.LCD_D6, False)
		self.pcf.set_pin(self.LCD_D7, False)

		# Define some device constants
		self.LCD_WIDTH = 16 # Maximum characters per line
		self.LCD_CHR = True
		self.LCD_CMD = False
		self.LCD_LINES = [0x80, 0xC0, 0x90, 0xD0]
 
		# Timing constants
		self.ENABLE_PULSE = 0.0005
		self.ENABLE_DELAY = 0.0005

	def init(self):
		# Initialise display
		self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
		self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
		self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
		self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
		self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
		self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
		time.sleep(self.ENABLE_DELAY)

	def toggle_enable(self):
		# Toggle enable
		time.sleep(self.ENABLE_DELAY)
		self.pcf.set_pin(self.LCD_EN, True)
		time.sleep(self.ENABLE_PULSE)
		self.pcf.set_pin(self.LCD_EN, False)
		time.sleep(self.ENABLE_DELAY)
		 
	def lcd_byte(self, byte, mode):
		# Send byte to data pins
		# byte = data
		# mode = True for character / False for command
 
		self.pcf.set_pin(self.LCD_RS, mode)
 
		# High byte
		self.pcf.set_pin(self.LCD_D4, False)
		self.pcf.set_pin(self.LCD_D5, False)
		self.pcf.set_pin(self.LCD_D6, False)
		self.pcf.set_pin(self.LCD_D7, False)
		if byte&0x10==0x10:
			self.pcf.set_pin(self.LCD_D4, True)
		if byte&0x20==0x20:
			self.pcf.set_pin(self.LCD_D5, True)
		if byte&0x40==0x40:
			self.pcf.set_pin(self.LCD_D6, True)
		if byte&0x80==0x80:
			self.pcf.set_pin(self.LCD_D7, True)
 
		# Toggle 'Enable' pin
		self.toggle_enable()

		# Low byte
		self.pcf.set_pin(self.LCD_D4, False)
		self.pcf.set_pin(self.LCD_D5, False)
		self.pcf.set_pin(self.LCD_D6, False)
		self.pcf.set_pin(self.LCD_D7, False)
		if byte&0x01==0x01:
			self.pcf.set_pin(self.LCD_D4, True)
		if byte&0x02==0x02:
			self.pcf.set_pin(self.LCD_D5, True)
		if byte&0x04==0x04:
			self.pcf.set_pin(self.LCD_D6, True)
		if byte&0x08==0x08:
			self.pcf.set_pin(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self.toggle_enable()

	def clear(self):
		self.lcd_byte(0x01, self.LCD_CMD)

	def string(self, line, text):
		# Send string to display
		text = text.ljust(self.LCD_WIDTH," ")
		self.lcd_byte(self.LCD_LINES[line-1], self.LCD_CMD)
		for i in range(self.LCD_WIDTH):
			self.lcd_byte(ord(text[i]), self.LCD_CHR)
