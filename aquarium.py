#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# Aquarium modules
#========================================================
#aquaWebVersion = "0.00"    # First lines
aquaWebVersion  = "0.01"    # aquarium as a class

import logging
import domoWebModule
import dataLogger
import gpioDevice
import string

from oneWireDevice import *

#=============================================================
# An aquarium module with
# . a 1wire thermoter in the water
# . 
#=============================================================
class aquarium(domoWebModule.domoWebModule) :

   # Available actions
   actions = ["lightOn", 'lightOff', 'pumpOn', 'pumpOff']

   def __init__(self, name, html="aquarium.html") :
      domoWebModule.domoWebModule.__init__(self, name, html)
#      self.logger = logging.getLogger('domoweb')
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

            self.logger.info("Aquarium waterTemp : " + value + " created")

         # Light switch
         if ('lightswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            print "Aquarium lightSwitch : " + value
            self.lightSwitch = createSwitch(value)

            self.logger.info(self.name+".lightSwitch : " + value + " created")


         # Pump switch
         if ('pumpswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            self.pumpSwitch = createSwitch(value)

            self.logger.info(self.name+".pumpSwitch : " + value + " created")


         # Room thermometer
         if ('roomtemp' == option) :
            roomTemp = (value) # WARNING ???
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.roomThermometer = createThermometer(value)
            self.logger.info("Aquarium waterTemp : " + value + " created")

      # Then we use the parent method
      domoWebModule.domoWebModule.setOptions(self, optionList)

   # Build a dictionary with local parameters
   def templateData(self):
      # Generic data
      templateData = domoWebModule.domoWebModule.templateData(self)

      templateData['waterTemp'] = self.waterThermometer.getTemperature()
      if (hasattr(self, 'roomThermometer')) :
         templateData['roomTemp'] = self.roomThermometer.getTemperature()

      # Building history
      templateData['tempHist'] = []
      
      # Building waterTemp history
      templateData['tempHist'].append(("Eau", self.waterThermometer.getHistory()))

      # Building airTemp history
      templateData['tempHist'].append(("Air", self.roomThermometer.getHistory()))

      # Pool light
      templateData['lightStatus'] = self.lightSwitch.getValue()

      # Pump
      templateData['pumpStatus'] = self.pumpSwitch.getValue()

      return templateData

   @domoWebModule.domoWebModuleAction
   def lightOn(self):
      self.logger.info(self.name + " : light on")
      self.lightSwitch.on()                                          
   
   @domoWebModule.domoWebModuleAction
   def lightOff(self):
      self.logger.info(self.name + " : light off")
      self.lightSwitch.off()

   def pumpOn(self):
      self.logger.info(self.name + " pump on")
      self.pumpSwitch.on()
   
   def pumpOff(self):
      self.logger.info(self.name + " pump off")
      self.pumpSwitch.off()

   @property
   @domoWebModule.domoWebModuleAttribute
   def test(self) :
      return self.__test

   @test.setter
   def test(self, val):
      self.__test = val
      
