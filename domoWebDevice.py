#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
import ConfigParser
import urllib
import string
import datetime

import oneWireDevice
from domoWebDataCache import *
import domoTask

#========================================================
# High level devices (thermometer, switch, ...)
#========================================================

#--------------------------------------------------------
# A basic device.
#
# A device can give a value with getValue()
# When a device is created, an history is built and values
# are automatically logged
#--------------------------------------------------------
class domoWebDevice() :
   def __init__(self) :
      self.historic = domoWebCircularDataCache(24*12)
      self.runPeriodicGetData(datetime.timedelta(seconds=300))

   def logData(self) :
      value = self.getValue()
      self.historic.cacheData((int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()*1000), value))
      
   def runPeriodicGetData(self, delaySec) :
      domoTask.queueTask(0, domoWebDevice.logData, self, delaySec)
      
   def getHistory(self) :
      return self.historic.getData()

#========================================================
# A basic on/off device
#========================================================
class domoWebSwitchDevice(domoWebDevice) :
   def __init__(self) :
      domoWebDevice.__init__(self)
      self.status = 0
      
   def on(self) :
      print " == domoWebSwitchDevice ON"
      self.status = 1
      
   def off(self) :
      print " == domoWebSwitchDevice OFF"
      self.status = 0

   def getValue(self) :
      print " == domoWebSwitchDevice GET"
      return self.status
   
#--------------------------------------------------------
# A remote switch device
#--------------------------------------------------------
class remoteSwitchDevice(domoWebSwitchDevice) :
   def __init__(self, urlOn, urlOff, urlStatus=None) :
      domoWebSwitchDevice.__init__(self)
      self.urlOn = urlOn
      self.urlOff = urlOff
      if (urlStatus is None) :
         self.statusSrc = None
      else :
         self.statusSrc = domoWebReadOnlyRemoteDevice(urlStatus)

   def on(self) :
      socket = urllib.urlopen(self.urlOn)
      domoWebSwitchDevice.on(self)

   def off(self) :
      socket = urllib.urlopen(self.urlOff)
      domoWebSwitchDevice.off(self)
  
   def getValue(self) :
      print("remoteSwitchDevice.getValue")
      if (self.statusSrc is None) :
         print("   cached value")
         return int(self.domoWebSwitchDevice())
      else :
         print("   get remote value")
         print self.statusSrc.getValue()
         return int(self.statusSrc.getValue())
   
#========================================================
# A thermometer can give ... temperatures !
#========================================================
class domoWebThermometer(domoWebDevice) :
   def __init__(self) :
      domoWebDevice.__init__(self)

   def getValue(self) :
      return self.getTemperature()
      
#--------------------------------------------------------
# A remote thermometer
#--------------------------------------------------------
class remoteThermometer(domoWebThermometer) :
   def __init__(self, url) :
      # First of all, this is a thermometer
      domoWebThermometer.__init__(self)

      self.source = domoWebReadOnlyRemoteDevice(url)

   def getTemperature(self) :
      value = self.source.getValue()
      return value

#--------------------------------------------------------
#   Create a thermometer from a description.
# . oneWire,address
# . remote,url
#--------------------------------------------------------
def createThermometer(desc) :
   lines = string.split(desc, ",")
   if (lines[0] == "remote") :
      return remoteThermometer(lines[1])
   elif (lines[0] == "oneWire") :
      return oneWireDevice.oneWireThermometer(lines[1])
   
#--------------------------------------------------------
#   Create a switch from a description :
# . oneWire,address
# . remote,urlOn,urlOff
# . fake                 (does nothing, debuging purpose)
#--------------------------------------------------------
def createSwitch(desc) :
   lines = string.split(desc, ",")
   if (lines[0] == "remote") :
#      print "*** A remote switch "
#      print "    -> " + lines[1]
#      print "    -> " + lines[2]
#      print "    -> " + lines[3]
      return remoteSwitchDevice(lines[1], lines[2],lines[3])
   elif (lines[0] == "fake") :
      return domoWebSwitchDevice()
   else :
      print "*** A FAIRE ***"
      gpioDevice.gpioDevice(int(value), gpioDevice.IN, gpioDevice.OFF)
      return None
   





#--------------------------------------------------------
# A basic read only device  (WARNING : to remove)
#--------------------------------------------------------
class domoWebReadOnlyDevice() :
   def __init__(self) :
      pass
   def getValue(self) :
      pass
    
#--------------------------------------------------------
# A remote read only device  (WARNING : to remove)
#--------------------------------------------------------
class domoWebReadOnlyRemoteDevice(domoWebReadOnlyDevice) :
   def __init__(self,url) :
      domoWebReadOnlyDevice.__init__(self)
      self.url = url

   # Re definition of domoWebReadOnlyDevice attibutes
   def getValue(self) :
      logger = logging.getLogger('domoweb').debug("Reading " + self.url)
      try :
         socket = urllib.urlopen(self.url)
         return socket.read()
      except IOError :
         
         return "0"
  
