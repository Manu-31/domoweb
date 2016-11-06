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
   actions = ["lightOn", 'lightOff', 'pumpOn', 'pumpOff', "robotOn", 'robotOff']
#   actions = ["lightOn", 'lightOff', 'pumpOn', 'pumpOff', "robotOn", 'robotOff', 'pHControlOn', 'pHControlOff']

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
         # Water thrmometer
         if ('watertemp' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.waterThermometer = createThermometer(value)

            self.logger.info(self.name+".waterTemp : " + value + " created")

         # Outside thermometer
         if ('outsidetemp' == option) :
            outsideTemp = (value)
            i = optionList.index((option, value))
            del optionList[i]

            # create a thermometer
            self.outsideThermometer = createThermometer(value)
            self.logger.info(self.name+".outsideTemp : " + value + " created")

         # Light switch
         if ('lightswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            self.lightSwitch = createSwitch(value)

            self.logger.info(self.name+".lightSwitch : " + value + " created")

         # Pump switch
         if ('pumpswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            self.pumpSwitch = createSwitch(value)

            self.logger.info(self.name+".pumpSwitch : " + value + " created")
            
         # Ph control switch
         if ('phcontrolswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            self.pHControlSwitch = createSwitch(value)

            self.logger.info(self.name+".pHControlSwitch : " + value + " created")

         # Robot switch
         if ('robotswitch' == option) :
            i = optionList.index((option, value))
            del optionList[i]

            # create a switch
            self.robotSwitch = createSwitch(value)

            self.logger.info(self.name+".robotSwitch : " + value + " created")
            
      # Then we use the parent method
      domoWebModule.domoWebModule.setOptions(self, optionList)

   # Build a dictionary with local parameters
   def templateData(self) :
      templateData = {'domoWebModuleName' : self.name}

      # Temperatures
      templateData['waterTemp'] = round(float(self.waterThermometer.getTemperature()), 1)
      if (hasattr(self, 'outsideThermometer')) :
         templateData['outsideTemp'] = round(float(self.outsideThermometer.getTemperature()), 1)
                                             
      # Termperature history
      templateData['tempHist'] = []
      
      # Building waterTemp history
      templateData['tempHist'].append(("Eau", self.waterThermometer.getHistory()))

      # Building airTemp history
      templateData['tempHist'].append(("Air", self.outsideThermometer.getHistory()))

      # Pool light
      templateData['lightStatus'] = self.lightSwitch.getValue()

      # Pump
      templateData['pumpStatus'] = self.pumpSwitch.getValue()

      # pH control
      templateData['pHControlStatus'] = self.pHControlSwitch.getValue()

      # Robot
      templateData['robotStatus'] = self.robotSwitch.getValue()


      return templateData

   def lightOn(self):
      self.logger.info(self.name + " : light on")
      self.lightSwitch.on()                                          
   
   def lightOff(self):
      self.logger.info(self.name + " : light off")
      self.lightSwitch.off()

   def pumpOn(self):
      self.logger.info(self.name + " pump on")
      self.pumpSwitch.on()
   
   def pumpOff(self):
      self.logger.info(self.name + " pump off")
      self.pumpSwitch.off()

   def robotOn(self):
      self.logger.info(self.name + " robot on")
      self.robotSwitch.on()
   
   def robotOff(self):
      self.logger.info(self.name + " robot off")
      self.robotSwitch.off()

   @domoWebModule.domoWebModuleAction
   def pHControlOn(self):
      self.logger.info(self.name + " : pH control on")
      self.pHControlSwitch.on()                                          
      
   @domoWebModule.domoWebModuleAction
   def pHControlOff(self):
      self.logger.info(self.name + " : pH control off")
      self.pHControlSwitch.off()

