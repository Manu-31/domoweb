#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# gpio devices for domoweb
#========================================================

try:
    import RPi.GPIO as gpio
except ImportError:
   import FakeRPi.GPIO as gpio

from domoWebDevice import *
   
logger = None
debugFlags = {}

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

#--------------------------------------------------------
# A switch
#--------------------------------------------------------
class gpioSwitch(gpioDevice, domoWebSwitchDevice) :
   def __init__(self, name, pinNum=None, l=[]) :
      if ('gpio' in debugFlags) :
         logger.debug("gpioSwitch.__init__("+name+")")
      gpioDevice.__init__(self, pinNum, OUT, OFF)
      domoWebSwitchDevice.__init__(self, name)
      # WARNING : A quoi ça sert ?
      #self.addAttribute('on', "")         
      #self.addAttribute('off', "")

   def on(self) :
     if ('gpio' in debugFlags) :
        logger.debug("gpioSwitch.on("+self.name+")")
     domoWebSwitchDevice.on(self)
     
   def offswitch(self) :
     if ('gpio' in debugFlags) :
        logger.debug("gpioSwitch.off("+self.name+")")
     domoWebSwitchDevice.off(self)

#========================================================
# module init
#========================================================
def gpioDeviceInit(c, l, d) :
   global debugFlags
   global logger
   logger = l
   debugFlags = d
   
   if (('gpio' in debugFlags) or ('modules' in debugFlags)) :
      logger.info("Initializing gpio subsystem")
   
   gpio.setwarnings(True) 
   gpio.setmode(gpio.BOARD)

