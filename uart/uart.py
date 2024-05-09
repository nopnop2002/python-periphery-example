#!/usr/bin/python
#-*- encoding: utf-8 -*-
import signal
import argparse
from periphery import Serial

def handler(signal, frame):
	global running
	print('handler')
	running = False

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', help="device file name", default='/dev/tty')
	parser.add_argument('-b', '--baudrate', type=int, help="baudrate", default=115200)
	parser.add_argument('-p', '--print', type=int, help="print debug", default=0)
	args = parser.parse_args()

	
	# Open device with baudrate 115200, and defaults of 8N1, no flow control
	print("device={}".format(args.device))
	print("baudrate={}".format(args.baudrate))
	#serial = Serial("/dev/ttyS4", 115200)
	serial = Serial(args.device, args.baudrate)
	DEBUG = args.print

	while running:
		serial.write(b"Hello World!")

		# Read up to 128 bytes with 1000ms timeout
		buf = serial.read(128, 1.0)
		if(DEBUG): print("len(buf)={}".format(len(buf)))
		if (len(buf) == 0):
			continue
		if(DEBUG): print("type(buf)={}".format(type(buf)))
		if (type(buf) is bytes):
			buf=buf.decode('utf-8')
		print("read {:d} bytes: [{}]".format(len(buf), buf))

	serial.close()

