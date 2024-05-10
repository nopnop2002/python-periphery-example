"""
python-periphery 1602 LCD sample

I ported from here
https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
"""
#!/usr/bin/python
#-*- encoding: utf-8 -*-
import time
from periphery import GPIO

class hdd44780:
	def __init__(self, rs, enable, d4, d5, d6, d7):	
		# Define GPIO to LCD mapping
		self.GPIO_RS = GPIO(rs, "out")
		self.GPIO_ENABLE = GPIO(enable, "out")
		self.GPIO_D4 = GPIO(d4, "out")
		self.GPIO_D5 = GPIO(d5, "out")
		self.GPIO_D6 = GPIO(d6, "out")
		self.GPIO_D7 = GPIO(d7, "out")

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
		self.GPIO_ENABLE.write(True)
		time.sleep(self.ENABLE_PULSE)
		self.GPIO_ENABLE.write(False)
		time.sleep(self.ENABLE_DELAY)
		 
	def lcd_byte(self, byte, mode):
		# Send byte to data pins
		# byte = data
		# mode = True for character / False for command
 
		self.GPIO_RS.write(mode) # RS
 
		# High byte
		self.GPIO_D4.write(False)
		self.GPIO_D5.write(False)
		self.GPIO_D6.write(False)
		self.GPIO_D7.write(False)
		if byte&0x10==0x10:
			self.GPIO_D4.write(True)
		if byte&0x20==0x20:
			self.GPIO_D5.write(True)
		if byte&0x40==0x40:
			self.GPIO_D6.write(True)
		if byte&0x80==0x80:
			self.GPIO_D7.write(True)
 
		# Toggle 'Enable' pin
		self.toggle_enable()

		# Low byte
		self.GPIO_D4.write(False)
		self.GPIO_D5.write(False)
		self.GPIO_D6.write(False)
		self.GPIO_D7.write(False)
		if byte&0x01==0x01:
			self.GPIO_D4.write(True)
		if byte&0x02==0x02:
			self.GPIO_D5.write(True)
		if byte&0x04==0x04:
			self.GPIO_D6.write(True)
		if byte&0x08==0x08:
			self.GPIO_D7.write(True)

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
