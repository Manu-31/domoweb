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

            self.logger.info("Aquarium waterTemp : " + value + " created")

         # Gpio light switch
         if ('lightswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a gpioDevice
            print "Aquarium lightSwitch : " + value
            self.lightSwitch = gpioDevice.gpioDevice(int(value), gpioDevice.IN, gpioDevice.OFF)

            self.logger.info("Aquarium lightSwitch : " + value + " created")

         # Room thermometer
         if ('roomtemp' == option) :
            roomTemp = (value)
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.roomThermometer = createThermometer(value)
            self.logger.info("Aquarium waterTemp : " + value + " created")
       
      # Then we use the parent method
      domoWebModule.domoWebModule.setOptions(self, optionList)

   # Build a dictionary with local parameters
   def templateData(self):
      templateData = {}
      templateData['waterTemp'] = self.waterThermometer.getTemperature()
      if (hasattr(self, 'roomThermometer')) :
         templateData['roomTemp'] = self.roomThermometer.getTemperature()
      templateData['etatEclairage'] = self.etatEclairage
      templateData['etatPompe'] = self.etatPompe

      # Building history
      templateData['tempHist'] = []
      
      # Building waterTemp history
      templateData['tempHist'].append(("Eau", self.waterThermometer.getHistory()))

      # Building airTemp history
      templateData['tempHist'].append(("Air", self.roomThermometer.getHistory()))

#      self.tempLogger.logData({'waterTemp': templateData['waterTemp']}) # WARNING : it was a test
      return templateData

   def lightOn(self):
      self.etatEclairage = 1
      print "On allume"
   
   def lightOff(self):
      self.etatEclairage = 0
      print "On etteint"   

   def pumpOn( self):
      self.etatPompe = 1
      print "On pompe"
   
   def pumpOff(self):
      self.etatPompe = 0
      print "On coupe"   
