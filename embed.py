#!/usr/bin/python3

import RPi.GPIO as GPIO

led = 13 # use GPIO 13 pin for demo

GPIO.setmode(GPIO.BCM) # use GPIO layout
GPIO.setup(led, GPIO.OUT)

# logics for detecting heartbeat below
