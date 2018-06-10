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
   def __init__(self, address) :
      self.setAddress(address)

   def setAddress(self, address) :
      self.addAttribute('address', address)

#--------------------------------------------------------
# A thermometer
#--------------------------------------------------------
class oneWireThermometer(oneWireDevice, domoWebThermometer) :
   def __init__(self, name, address=None, l=[]) :
      if ('oneWire' in debugFlags) :
         self.logger.debug("oneWireThermometer.__init__("+name+", ...)")
      if  l :
         address = l[0]

      # First of all, this is a thermometer
      domoWebThermometer.__init__(self, name)

      # It is also a 1wire device
      oneWireDevice.__init__(self, address)

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
    debugFlags = d

    if (('oneWire' in debugFlags) or ('modules' in debugFlags)) :
      logger.info("Initializing oneWire subsystem")


    oneWireDevice.oneWireRootDir = config.get('1wirefs', 'rootDir')
    oneWireDevice.logger = logger

   
