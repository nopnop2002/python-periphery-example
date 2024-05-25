#!/usr/bin/python
#-*- encoding: utf-8 -*-
import sys
import argparse
import time
from hdd44780 import hdd44780
 
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', help="device file name", default='/dev/i2c-1')
	parser.add_argument('--addr', type=lambda x: int(x, 16), help="i2c address", default=0x20)
	parser.add_argument('--text1', help="text of line1", default='')
	parser.add_argument('--text2', help="text of line2", default='')
	parser.add_argument('--text3', help="text of line3", default='')
	parser.add_argument('--text4', help="text of line4", default='')
	parser.add_argument('--texts', type=str, nargs="*", help='a list of text')
	args = parser.parse_args()	
	
	text1 = args.text1
	text2 = args.text2
	text3 = args.text3
	text4 = args.text4
	if args.texts is not None:
		print("texts={} {}".format(len(args.texts),args.texts))
		text1 = args.texts[0]
		if len(args.texts) > 1: text2 = args.texts[1]
		if len(args.texts) > 2: text3 = args.texts[2]
		if len(args.texts) > 3: text4 = args.texts[3]

	lcd = hdd44780(args.device, args.addr)

	# Inisialize display
	lcd.init()
	# Clear display
	lcd.clear()
	# Show display
	len1 = len(text1)
	len2 = len(text2)
	len3 = len(text3)
	len4 = len(text4)
	if len3 or len4:
		lcd.string(1, text1)
		lcd.string(2, text2)
		lcd.string(3, text3)
		lcd.string(4, text4)
	elif len1 or len2:
		lcd.string(1, text1)
		lcd.string(2, text2)
