#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
#   Interface web pour mes petits jouets domotifiants.
#
#   A faire
#
#   0.2
#      Une page avec des mesures de température, ...
#
# A voir http://sharedmemorydump.net/logging-data-temperature-with-raspberry-pi
# 
#=============================================================

#domowebVersion = "0.00"   # First skeleton
domowebVersion = "0.01"    # domoWebModules are now classes

#=============================================================
# Some imports
#=============================================================
import ConfigParser
import os
import logging

import oneWireDevice
import webui
import domoWebModule
import gpioDevice
import domoTask
import domoWebDataCache
  
#=============================================================
# Let's go
#=============================================================

#-------------------------------------------------------------
# Lecture du fichier de configuration
#
# On va chercher la configuration dans les fichiers suivants et dans
# cet ordre
#   /etc/domoweb.cfg
#   ${HOME}/.domoweb.cfg
#-------------------------------------------------------------
config = ConfigParser.ConfigParser()
config.optionxform = str

config.read(['/etc/domoweb.cfg', os.path.expanduser('~/.domoweb.cfg')])

#-------------------------------------------------------------
# Default debuging
#-------------------------------------------------------------
logFileName = config.get('debug', 'logFileName')
logConsole =  config.getboolean('debug', 'logConsole')
debugFlags = config.get('debug', 'debugFlags')

#-------------------------------------------------------------
# Logging system configuration
#-------------------------------------------------------------
if (logConsole) :
   logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s',
                       level=logging.DEBUG)
else :
   logging.basicConfig(filename=logFileName,
                       format='%(asctime)s - %(levelname)s:%(message)s',
                       level=logging.DEBUG)
logger = logging.getLogger('domoweb')
logger.info("DomoWeb version " + domowebVersion + " running")

domoWebModule.domoWebModule.debugFlags = debugFlags

#-------------------------------------------------------------
# cache initialisation
#-------------------------------------------------------------
domoWebDataCache.domoWebDataCacheInit(config, logger, debugFlags)

#-------------------------------------------------------------
# Task mgt init
#-------------------------------------------------------------
domoTask.domoTaskInit(logger, debugFlags)
   
#-------------------------------------------------------------
# 1wire initialization
#-------------------------------------------------------------
oneWireDevice.oneWireInit(config, logger, debugFlags)

#-------------------------------------------------------------
# gpioDevices init
#-------------------------------------------------------------
gpioDevice.gpioDeviceInit(config, logger, debugFlags)

#-------------------------------------------------------------
# Configuration of displayed tabs
#-------------------------------------------------------------
webui.buildWebui(config, logger, debugFlags)

