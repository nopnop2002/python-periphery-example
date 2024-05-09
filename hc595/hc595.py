"""
python-periphery hc595 sample
"""
#!/usr/bin/python
#-*- encoding: utf-8 -*-
import time
from periphery import GPIO

class hc595:
	register_type = '74HC595'

	"""
	data_pin => pin 14 on the 74HC595
	latch_pin => pin 12 on the 74HC595
	clock_pin => pin 11 on the 74HC595
	"""
	def __init__(self, data_pin, latch_pin, clock_pin):
		self.gpio_data_pin = GPIO(data_pin,"out")
		self.gpio_latch_pin = GPIO(latch_pin,"out")
		self.gpio_clock_pin = GPIO(clock_pin,"out")
		self.outputs = [0] * 8

	"""
	output_number => Value from 0 to 7 pointing to the output pin on the 74HC595
	0 => Q0 pin 15 on the 74HC595
	1 => Q1 pin 1 on the 74HC595
	2 => Q2 pin 2 on the 74HC595
	3 => Q3 pin 3 on the 74HC595
	4 => Q4 pin 4 on the 74HC595
	5 => Q5 pin 5 on the 74HC595
	6 => Q6 pin 6 on the 74HC595
	7 => Q7 pin 7 on the 74HC595
	value => a state to pass to the pin, could be HIGH or LOW
	"""
	def setOutput(self, output_number, value):
		try:
			self.outputs[output_number] = value
		except IndexError:
			raise ValueError("Invalid output number. Can be only an int from 0 to 7")

	def setOutputs(self, outputs):
		if 8 != len(outputs):
			raise ValueError("setOutputs must be an array with 8 elements")

		self.outputs = outputs

	def showOutputs(self):
		print(self.outputs)

	def latch(self):
		self.gpio_latch_pin.write(False)

		for i in range(7, -1, -1):
			self.gpio_clock_pin.write(False)
			if (self.outputs[i] == 0):
			  self.gpio_data_pin.write(False)
			if (self.outputs[i] == 1):
			  self.gpio_data_pin.write(True)
			self.gpio_clock_pin.write(True)
		self.gpio_latch_pin.write(True)

	def Output(self, output_number, value):
		self.setOutput(output_number, value)
		self.latch()
