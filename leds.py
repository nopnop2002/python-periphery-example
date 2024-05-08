#!/usr/bin/python
#-*- encoding: utf-8 -*-
from periphery import LED
import time
import signal
import sys
import argparse

def handler(signal, frame):
	global running
	print('handler')
	running = False

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	running = True

	parser.add_argument('-d', '--device', help='Onboard LED device', default="leds")
	args = parser.parse_args()
	signal.signal(signal.SIGINT, handler)
	# Open On Board LED "led0" with initial state off
	led0 = LED(args.device, False)

	while running:
		led0.write(0)
		time.sleep(1.0);
		led0.write(1)
		time.sleep(1.0);

	led0.close()
