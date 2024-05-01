#!/usr/bin/python
#-*- encoding: utf-8 -*-
from periphery import GPIO
import time
import signal
import sys
import argparse

running = True

def handler(signal, frame):
	global running
	print('handler')
	running = False

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--gpio', type=int, help='GPIO to blink', default=1)
	args = parser.parse_args()

	signal.signal(signal.SIGINT, handler)
	gpio_out = GPIO(args.gpio, "out")

	while running:
		gpio_out.write(False)
		time.sleep(1.0)
		gpio_out.write(True)
		time.sleep(1.0)

	gpio_out.write(False)
	gpio_out.close()
