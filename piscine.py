#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# Piscine modules
#========================================================
#aquaWebVersion = "0.00"    # First lines
aquaWebVersion  = "0.01"    # piscine as a class

import logging
import domoWebModule
import dataLogger
import gpioDevice
import string

from oneWireDevice import *

#=============================================================
# An piscine module with
# . a 1wire thermoter in the water
# . 
#=============================================================
class piscine(domoWebModule.domoWebModule) :

   # Available actions
   actions = ["lightOn", 'lightOff', 'pumpOn', 'pumpOff']

   def __init__(self, name, html="piscine.html") :
      domoWebModule.domoWebModule.__init__(self, name, html)
      self.logger = logging.getLogger('domoweb')
      self.etatEclairage = 0
      self.etatPompe = 0
      self.tempLogger = dataLogger.dataLogger()

   # Option reading
   def setOptions(self, optionList):
      # We get specific options and remove them from the list
      ol = list(optionList)
      for option, value in ol :
         # 1wire thermometer address
         if ('watertemp' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.waterThermometer = createThermometer(value)

            self.logger.info("Piscine waterTemp : " + value + " created")

         # Gpio light switch
         if ('lightswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a gpioDevice
            self.lightSwitch = gpioDevice.gpioDevice(value, gpioDevice.IN, gpioDevice.OFF)

            self.logger.info("Piscine lightSwitch : " + value + " created")

         # Outside thermometer
         if ('outsidetemp' == option) :
            roomTemp = (value)
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.outsideThermometer = createThermometer(value)
            self.logger.info("Piscine outsideTemp : " + value + " created")

         # Pump switch
         if ('pumpswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a gpioDevice
            self.pumpSwitch = createSwitch(value)

            self.logger.info("Piscine lightSwitch : " + value + " created")
            
      # Then we use the parent method
      domoWebModule.domoWebModule.setOptions(self, optionList)

   # Build a dictionary with local parameters
   def templateData(self):
      templateData = {}
      templateData['waterTemp'] = round(float(self.waterThermometer.getTemperature()), 1)
      if (hasattr(self, 'roomThermometer')) :
         templateData['roomTemp'] = self.roomThermometer.getTemperature()
      templateData['etatEclairage'] = self.etatEclairage
      templateData['etatPompe'] = self.etatPompe
      self.tempLogger.logData({'waterTemp': templateData['waterTemp']})
      return templateData

   def lightOn(self):
      self.etatEclairage = 1
      print "On allume"
   
   def lightOff(self):
      self.etatEclairage = 0
      print "On etteint"   

   def pumpOn(self):
      self.etatPompe = 1
      self.logger.info(self.name + " pump on")
      self.pumpSwitch.on()
   
   def pumpOff(self):
      self.etatPompe = 0
      self.logger.info(self.name + " pump off")
      self.pumpSwitch.off()

