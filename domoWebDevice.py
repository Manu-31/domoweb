#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# low level devices (data source)
#========================================================
import ConfigParser
import urllib
import string
import datetime

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
      self.historique = []

   def getTemperature(self) :
      value = self.source.getValue()
      self.historique.append(((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()*1000, value))
      return value

   def getHistory(self) :
      result = {'name' : 'temp',
                't0' : self.historique[0][0],
                'p' : datetime.timedelta(minutes=5),
                'data' : self.historique}
      return result
   
  
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

   
