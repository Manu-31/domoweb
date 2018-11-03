#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# 1wire devices
#========================================================
import ConfigParser
import datetime

from domoWebDevice import *

debugFlags = {}

class oneWireDevice :
   oneWireRootDir = '/sys/bus/w1/devices'
   def __init__(self, address=None) :
      self.address = address

   @property
   def address(self) :
      return self.__address

   @address.setter
   def address(self, address) :
      if address is not None :
         print "oneWireDevice address setter set to '"+str(address)+"'"
      else :
         print "oneWireDevice address setter set to 'None'"
      self.__address = address

#--------------------------------------------------------
# A thermometer
#--------------------------------------------------------
class oneWireThermometer(oneWireDevice, domoWebThermometer) :
   def __init__(self, name) :
      if (('oneWire' in debugFlags) or ('all' in debugFlags)):
         self.logger.debug("oneWireThermometer.__init__("+name+", ...)")

      # First of all, this is a thermometer
      domoWebThermometer.__init__(self, name)

      # It is also a 1wire device
      oneWireDevice.__init__(self)

      # As such, it has an address attribute
      self.turnAttribute('address')
      

   def read_temp_raw(self):
      if ('oneWire' in debugFlags) :
         self.logger.debug("oneWireThermometer.read_temp_raw("+self.name+")")
      try :
         deviceFile = oneWireDevice.oneWireRootDir + '/' + self.address + '/w1_slave'
         f = open(deviceFile, 'r')
         lines = f.readlines()
         f.close()
      except Exception :
         lines = {}
      if ('oneWire' in debugFlags) :
         self.logger.debug("oneWireThermometer.read_temp_raw("+self.name+") : ")
         for l in lines :
            self.logger.debug("     - '"+l+"'")
      return lines
 
   def readData(self) :
      lines = self.read_temp_raw()
      while ((len(lines) >= 3) and (lines[0].strip()[-3:] != 'YES')):
         time.sleep(0.2)
         lines = self.read_temp_raw()
      try :
         equals_pos = lines[1].find('t=')
         if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
      except Exception :
         temp_c = 0.0
      return temp_c

   # Re definition of domoWebReadOnlyDevice attibutes
   def getTemperature(self) :
      value = self.readData()
      return value

#========================================================
# Initialization of global parameters
#========================================================
def oneWireInit(config, logger, d) :
    global debugFlags

    debugFlags = d

    if (('oneWire' in debugFlags) or ('modules' in debugFlags) or ('all' in debugFlags)) :
      logger.info("Initializing oneWire subsystem")

    if (config.has_section('1wirefs')) :
       oneWireDevice.oneWireRootDir = config.get('1wirefs', 'rootDir')
       
    if (('oneWire' in debugFlags) or ('modules' in debugFlags) or ('all' in debugFlags)) :
      logger.info("   oneWire root is '"+oneWireDevice.oneWireRootDir+"'")

    oneWireDevice.logger = logger

   
