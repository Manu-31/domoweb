#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# gpio devices for domoweb
#========================================================

try:
    import RPi.GPIO as gpio
except ImportError:
   import FakeRPi.GPIO as gpio


IN = gpio.IN
OUT = gpio.OUT
ON = gpio.HIGH
OFF = gpio.LOW

class gpioDevice :
   def __init__(self, pinNum, direction, initValue) :
      self.pin = pinNum
      self.direction = direction
      gpio.setup(self.pin, self.direction)

   def setValue(self, value):
      gpio.output(self.pin, value)

def gpioDeviceInit() :
   gpio.setwarnings(True) 
   gpio.setmode(gpio.BOARD)

