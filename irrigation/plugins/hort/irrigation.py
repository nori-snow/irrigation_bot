# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

def wateringResponse(something):
	sec = int('{0}'.format(something))

	GPIO.setmode(GPIO.BCM)

	#PIN = 27
	PIN = 21

	GPIO.setup(PIN, GPIO.OUT)

	#GPIO.output(PIN, GPIO.HIGH)
	GPIO.output(PIN, 1)

	time.sleep(sec)

	#GPIO.output(PIN, GPIO.LOW)
	GPIO.output(PIN, 0)
		
	msg = '水やりを '+ str(sec) +' 秒行いました'

	return msg

