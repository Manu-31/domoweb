#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
import ConfigParser
import urllib
import string
import datetime

from domoWebDataCache import *
import domoTask
from domoWebModule import domoWebModule
import domoWebAction
import oneWireDevice
import domoWebLogBook

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
class domoWebDevice(domoWebModule) :
   def __init__(self, name, l=[]) :
      domoWebModule.__init__(self, name)

      # A buffer is created to store consecutive values
      self.historic = domoWebCircularDataCache(name+'-data-cache', 24*12)
      self.turnAttribute('historic')

      # A task is run to store on a periodic basis
      self.runPeriodicGetData(datetime.timedelta(seconds=300))

   # Store a data in the buffer
   def logData(self) :
      value = self.getValue()
      self.historic.cacheData(value)
      
   def runPeriodicGetData(self, delaySec) :
      domoTask.queueTask(0, domoWebDevice.logData, self, delaySec)

#========================================================
# A basic on/off device
#
# Any inheritent must override on/off/getValue
# One can override status setter, but must then override getter
#========================================================
class domoWebSwitchDevice(domoWebDevice) :
   actions = [ 'on', 'off']
   def __init__(self, name) :
      # It is a domoWebDevice
      domoWebDevice.__init__(self, name)

      # As such, it has a status attribute
      self.turnAttribute('status')

      self.__status = 0
      
   @property
   def status(self) :
      return self.getValue()

   @status.setter
   def status(self, st) :
      print "On change le status pour ..."
      if (st == 0) or (st == '0') or (st == 'off') :
         print "... Off"
         self.off()
      else :
         print "... On"
         self.on()
         
   def on(self) :
      if ('switch' in domoWebModule.debugFlags) :
         self.logger.debug(self.name+".on")
      self.__status = 1
      
   def off(self) :
      if ('switch' in domoWebModule.debugFlags) :
         self.logger.debug(self.name+".off")
      self.__status = 0

   def getValue(self) :
      if ('switch' in domoWebModule.debugFlags) :
         self.logger.debug(self.name+".getValue : "+str(self.status))
      return self.__status
   
   
#========================================================
# A thermometer can give ... temperatures !
#========================================================
class domoWebThermometer(domoWebDevice) :
   def __init__(self, name) :
      domoWebDevice.__init__(self, name)
      domoWebDevice.turnAttribute(self, 'temperature')

      domoWebDevice.addAttribute(self, 'actionLow', None)
      domoWebDevice.addAttribute(self, 'actionHigh', None)
      domoWebDevice.addAttribute(self, 'minimum', 20.0)
      domoWebDevice.addAttribute(self, 'maximum', 21.0)
      self.level = 1 # 0 < min < 1 < max < 2

   @property
   def temperature(self) :
      res = self.getTemperature()
      #print "??? " + str(res)
      if (res > self.maximum) :
         if (self.level != 2 ) :
            domoWebLogBook.logBookAddEvent("*** Houlà ça chauffe !")
            self.level = 2
            if (self.actionHigh is not None) :
               self.actionHigh.run()
      elif (res < self.minimum) :
         if (self.level != 0) :
            domoWebLogBook.logBookAddEvent("Hé ça caille !")
            self.level = 0
            if (self.actionLow is not None) :
               self.actionLow.run()
      else :
         if (self.level == 0):
            domoWebLogBook.logBookAddEvent("*** Ouf, ça se réchauffe ...")
            self.level = 1
         elif (self.level == 2) :
            domoWebLogBook.logBookAddEvent("*** Enfin, ça se raffraichi ...")
            self.level = 1
      return res
   
   def getValue(self) :
      return self.temperature
   
  
#========================================================
# Les remotes
#========================================================

#--------------------------------------------------------
# A remote device
#--------------------------------------------------------
class remoteDevice() :
   def __init__(self) :
      self.__url = None

   @property
   def url(self) :
      return self.__url

   @url.setter
   def url(self, url) :
      self.__url = url

   def getValue(self) :
      try :
         socket = urllib.urlopen(self.url)
         return socket.read()
      except IOError :
         return None 
      
#--------------------------------------------------------
# A remote thermometer
#--------------------------------------------------------
class remoteThermometer(domoWebThermometer, remoteDevice) :
   def __init__(self, name) :

      if (('remote' in debugFlags) or ('all' in debugFlags)):
         self.logger.debug("remoteThermometer.__init__("+name+")")
      
      # First of all, this is a thermometer
      domoWebThermometer.__init__(self, name)

      # It is also a remote device
      remoteDevice.__init__(self)
      
      # As such, it has an url attribute
      self.turnAttribute('url')

   def getTemperature(self) :
      value = remoteDevice.getValue(self)
      return value

#--------------------------------------------------------
# A remote switch
#--------------------------------------------------------
class remoteSwitch(domoWebSwitchDevice, remoteDevice) :
   def __init__(self, name) :

      if (('switch' in debugFlags) or ('remote' in debugFlags) or ('all' in debugFlags)):
         self.logger.debug("remoteSwitch.__init__("+name+")")
      
      # First of all, this is a switch
      domoWebSwitchDevice.__init__(self, name)

      # It is also a remote device
      remoteDevice.__init__(self)
      
      # As such, it has an url attribute (to read status)
      self.turnAttribute('url')

      # We need two URLs for on/off
      self.__urlOn = None
      self.__urlOff = None
      self.turnAttribute('urlOn')
      self.turnAttribute('urlOff')

   @property
   def urlOn(self) :
      return self.__urlOn

   @urlOn.setter
   def urlOn(self, url) :
      self.__urlOn = url

   @property
   def urlOff(self) :
      return self.__urlOff

   @urlOff.setter
   def urlOff(self, url) :
      self.__urlOff = url

   def on(self) :
      try :
         socket = urllib.urlopen(self.urlOn)
         return socket.read()  # WARNING ON S'EN FOUT
      except IOError :
         return None 

   def off(self) :
      try :
         socket = urllib.urlopen(self.urlOff)
         return socket.read()
      except IOError :
         return None 

   def getValue(self) :
      try :
         socket = urllib.urlopen(self.url)
         res = socket.read()
         if ((res == 1 ) or (res == "1") or (res == "on")or (res == "On")or (res == "ON")or (res == "yes")):
            return 1
         else :
            return 0
         
      except IOError :
         return None 


