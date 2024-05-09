#!/usr/bin/python
#-*- encoding: utf-8 -*-
import argparse
import time
from hc595 import hc595

if __name__ == '__main__':
	parser = argparse.ArgumentParser()	
	parser.add_argument('--data', type=int, help="DATA GPIO", default=23)
	parser.add_argument('--latch', type=int, help="LATCH GPIO", default=24)
	parser.add_argument('--clock', type=int, help="CLOCK GPIO", default=25)
	parser.add_argument('--delay', type=float, help="Delay time", default=0.1)
	args = parser.parse_args()	

	register = hc595(args.data, args.latch, args.clock)
	
	# Turn off all outputs
	register.setOutputs([0,0,0,0,0,0,0,0])	
	register.latch()	
	time.sleep(1)
	
	# Turn on QH from QA
	for i in range(8):
		print("Q{} ON".format(chr(i+0x41)))
		register.Output(i, 1)
		time.sleep(args.delay)

	# Turn on QA from QH
	time.sleep(1)
	for i in range(8):
		print("Q{} OFF".format(chr(7-i+0x41)))
		register.Output(7-i, 0)
		time.sleep(args.delay)
