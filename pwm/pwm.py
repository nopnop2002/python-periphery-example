#!/usr/bin/python
#-*- encoding: utf-8 -*-
from periphery import PWM
import time
import signal
import argparse

def handler(signal, frame):
	global running
	print('handler')
	running = False

if __name__=="__main__":
	signal.signal(signal.SIGINT, handler)
	running = True

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--chip', type=int, help='PWM chip number', default=10)
	parser.add_argument('-n', '--channell', type=int, help='PWM channell number', default=0)
	parser.add_argument('-f', '--freq', type=int, help='PWM frequency', default=1000)
	parser.add_argument('-d', '--duty', type=int, help='PWM duty', default=0)
	parser.add_argument('-p', '--polarity', help='PWM polarity', default="normal")
	args = parser.parse_args()

	# Open PWM chip
	print("chip={}".format(args.chip))
	print("channell={}".format(args.channell))
	print("freq={}".format(args.freq))
	print("duty={}".format(args.duty))
	print("polarity={}".format(args.polarity))
	pwm = PWM(args.chip, args.channell)  

	pwm.frequency = args.freq
	pwm.duty_cycle = args.duty
	pwm.polarity = args.polarity
	pwm.enable()

	direction = 1  
	_direction = -1

	while running:
		if (direction != _direction):
			print("direction={}".format(direction))
			_direction = direction
		pwm.duty_cycle += 0.01 * direction
		pwm.duty_cycle = round(pwm.duty_cycle, 2)
		if pwm.duty_cycle == 1.0:
			direction = -1
		elif pwm.duty_cycle == 0.0:
			direction = 1
			
		time.sleep(0.05) 

	pwm.close()
