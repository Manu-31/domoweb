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

#--------------------------------------------------------
# gpio level stuff
#--------------------------------------------------------
class gpioDevice :
   def __init__(self) :
      self.__direction = IN
      self.__pin = None

   @property
   def pin(self) :
      return self.__pin

   @pin.setter
   def pin(self, pin) :
      print "gpioDevice "+self.name+".pin = "+str(pin)
      self.__pin = int(pin)
      if (self.__direction is not None) :
         gpio.setup(int(self.__pin), self.__direction)
      
   @property
   def direction(self) :
      return self.__direction

   @direction.setter
   def direction(self, direction) :
      self.__direction = direction
      if (self.__pin is not None) :
         gpio.setup(int(self.__pin), self.__direction)

   @property
   def value(self)  :
      return gpio.input(self.pin)

   @value.setter
   def value(self, value):
      if (self.__pin is not None and self.__direction is not None) :
         if ((str(value) == "1") or (value == 1) or (value == "on") or (value == "Nn") or (value == "ON")):
            gpio.output(self.__pin, gpio.HIGH)
         else :
            gpio.output(self.__pin, gpio.LOW)

#--------------------------------------------------------
# A switch
#--------------------------------------------------------
class gpioSwitch(gpioDevice, domoWebSwitchDevice) :
   def __init__(self, name) :
      if (('gpio' in debugFlags)  or ('all' in debugFlags)) :
         logger.debug("gpioSwitch.__init__(name="+name+") IN")

      # It is a gpio device
      gpioDevice.__init__(self)
      self.direction = OUT 
      
      # It is a switch device
      domoWebSwitchDevice.__init__(self, name)

      # As such, it has a pin and a direction attribute
      self.turnAttribute('pin')
      self.turnAttribute('direction')

      if (('gpio' in debugFlags)  or ('all' in debugFlags)) :
         if ( self.pin is None) :
            logger.debug("gpioSwitch.__init__(name="+name+") pin = ???")
         else :
            logger.debug("gpioSwitch.__init__(name="+name+") pin = "+ str(self.pin))

   def on(self) :
     if (('gpio' in debugFlags)  or ('all' in debugFlags)) :
        logger.debug("gpioSwitch.on("+self.name+")")
     self.value = 1
     
   def off(self) :
     if (('gpio' in debugFlags) or ('all' in debugFlags)) :
        logger.debug("gpioSwitch.off("+self.name+")")
     self.value = 0

   def getValue(self) :
      return self.value


#========================================================
# module init
#========================================================
def gpioDeviceInit(c, l, d) :
   global debugFlags
   global logger
   logger = l
   debugFlags = d
   
   if (('gpio' in debugFlags) or ('modules' in debugFlags) or ('all' in debugFlags)) :
      logger.info("Initializing gpio subsystem")
   
   gpio.setwarnings(True) 
   gpio.setmode(gpio.BOARD)

