#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import argparse
import time
from LcdGpio import LcdGpio
 
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--rs', type=int, help="RS GPIO", default=23)
	parser.add_argument('--enable', type=int, help="ENABLE GPIO", default=24)
	parser.add_argument('--d4', type=int, help="D4 GPIO", default=14)
	parser.add_argument('--d5', type=int, help="D4 GPIO", default=15)
	parser.add_argument('--d6', type=int, help="D4 GPIO", default=17)
	parser.add_argument('--d7', type=int, help="D4 GPIO", default=18)
	parser.add_argument('--text1', help="text of line1", default='Hello!!')
	parser.add_argument('--text2', help="text of line2", default='World!!')
	parser.add_argument('--text3', help="text of line3", default='')
	parser.add_argument('--text4', help="text of line4", default='')
	parser.add_argument('--clear', action='store_true', help="clear all text")
	args = parser.parse_args()	
	#print("clear={}".format(args.clear))
	
	lcd = LcdGpio(args.rs, args.enable, args.d4, args.d5, args.d6, args.d7)

	# Inisialize display
	lcd.init()
	# Clear display
	lcd.clear()
	if args.clear is True:
		sys.exit()
	# Show display
	len1 = len(args.text1)
	len2 = len(args.text2)
	len3 = len(args.text3)
	len4 = len(args.text4)
	if len3 or len4:
		lcd.string(1, args.text1)
		lcd.string(2, args.text2)
		lcd.string(3, args.text3)
		lcd.string(4, args.text4)
	elif len1 or len2:
		lcd.string(1, args.text1)
		lcd.string(2, args.text2)
