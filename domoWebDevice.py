#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# low level devices (data source)
#========================================================
import ConfigParser
import urllib
import string

import oneWireDevice

#--------------------------------------------------------
# A basic read only device
#--------------------------------------------------------
class domoWebReadOnlyDevice() :
   def __init__(self) :
      pass
   def getValue(self) :
      pass
    
#--------------------------------------------------------
# A remote read only device
#--------------------------------------------------------
class domoWebReadOnlyRemoteDevice(domoWebReadOnlyDevice) :
   def __init__(self,url) :
      domoWebReadOnlyDevice.__init__(self)
      self.url = url

   # Re definition of domoWebReadOnlyDevice attibutes
   def getValue(self) :
      socket = urllib.urlopen(self.url)
      return socket.read()
  
#--------------------------------------------------------
# A basic on/off device
#--------------------------------------------------------
class domoWebSwitchDevice() :
   def __init__(self) :
      pass
   def on(self) :
      pass
   def off(self) :
      pass
    
#--------------------------------------------------------
# A remote switch device
#--------------------------------------------------------
class remoteSwitchDevice(domoWebSwitchDevice) :
   def __init__(self, urlOn, urlOff) :
      domoWebSwitchDevice.__init__(self)
      self.urlOn = urlOn
      self.urlOff = urlOff

   def on(self) :
      socket = urllib.urlopen(self.urlOn)

   def off(self) :
      socket = urllib.urlopen(self.urlOff)
  
#========================================================
# high level devices
#========================================================
class domoWebThermometer :
   def __init__(self) :
      pass

   def getTemperature() :
      pass

#--------------------------------------------------------
# A remote thermometer
#--------------------------------------------------------
class remoteThermometer(domoWebThermometer) :
   def __init__(self, url) :
      self.source = domoWebReadOnlyRemoteDevice(url)

   def getTemperature(self) :
      return self.source.getValue()
  
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
#   Create a switch from a description.
# . oneWire,address
# . remote,urlOn,urlOff
#--------------------------------------------------------
def createSwitch(desc) :
   lines = string.split(desc, ",")
   if (lines[0] == "remote") :
      return remoteSwitchDevice(lines[1], lines[2])

   
