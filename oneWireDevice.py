#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# 1wire devices
#========================================================
import ConfigParser
from domoWebDevice import *

class oneWireDevice :
   oneWireRootDir = '/sys/bus/w1/devices'
   def __init__(self, address) :
      self.address = address

class oneWireThermometer(oneWireDevice, domoWebThermometer) :
   def __init__(self, address) :
      domoWebThermometer.__init__(self)
      oneWireDevice.__init__(self, address)
      self.deviceFile = oneWireDevice.oneWireRootDir + '/' + address + '/w1_slave'

   def read_temp_raw(self):
      f = open(self.deviceFile, 'r')
      lines = f.readlines()
      f.close()
      return lines
 
   def getTemperature(self) :
      lines = self.read_temp_raw()
      while lines[0].strip()[-3:] != 'YES':
         time.sleep(0.2)
         lines = self.read_temp_raw()
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0
         return temp_c

   # Re definition of domoWebReadOnlyDevice attibutes
   def getValue(self) :
      return getTemperature(self)
   
# Initialization of global parameters
def oneWireInit(config, logger) :
    oneWireDevice.oneWireRootDir = config.get('1wirefs', 'rootDir')
    oneWireDevice.logger = logger
