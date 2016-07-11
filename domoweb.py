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

config.read(['/etc/domoweb.cfg', os.path.expanduser('~/.domoweb.cfg')])

#  Le debogage
logFileName = config.get('debug', 'logFileName')
logConsole =  config.getboolean('debug', 'logConsole')

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

#-------------------------------------------------------------
# cache initialisation
#-------------------------------------------------------------
domoWebDataCache.domoWebDataCacheInit(logger)

#-------------------------------------------------------------
# 1wire initialization
#-------------------------------------------------------------
oneWireDevice.oneWireInit(config, logger)

#-------------------------------------------------------------
# gpioDevices init
#-------------------------------------------------------------
gpioDevice.gpioDeviceInit()

#-------------------------------------------------------------
# Configuration of displayed tabs
#-------------------------------------------------------------
webui.buildWebui(config)

