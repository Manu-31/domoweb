#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================

#=============================================================
# Some imports
#=============================================================
import os
import argparse

import domoWebUser
import oneWireDevice
import webui
import domoWebModule
import domoWebModuleMgt
import gpioDevice
import domoTask
import domoWebDataCache

from domoWebConfigParser import *
import domoWebLogger 

#=============================================================
# Let's go
#=============================================================

#-------------------------------------------------------------
# Parsing args
#-------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config',
                    dest='configFileName')

args=parser.parse_args()

#-------------------------------------------------------------
# Load configuration from a file. This function builds up the
# domoWebConfigParser.config structure
#-------------------------------------------------------------
configParserInit(args.configFileName)

#-------------------------------------------------------------
# Loggin facility initialization
#-------------------------------------------------------------
domoWebLogger.domoWebLoggerInit(config)
logger = domoWebLogger.logger
debugFlags = domoWebLogger.debugFlags

#-------------------------------------------------------------
# User management
#-------------------------------------------------------------
domoWebUser.domoWebUserInit(config, logger, debugFlags)

#-------------------------------------------------------------
# cache initialisation
#-------------------------------------------------------------
domoWebDataCache.domoWebDataCacheInit(config, logger, debugFlags)

#-------------------------------------------------------------
# Task management init
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
# domoWebModuleMgt  initalization
#-------------------------------------------------------------
domoWebModuleMgt.domoWebModuleManagementInit(config, logger, debugFlags)

#-------------------------------------------------------------
# Everything should have been initialized, we can start asynchronous
# tasks 
#-------------------------------------------------------------
domoTask.domoTaskStart()
   
#-------------------------------------------------------------
# Configuration of displayed tabs
#-------------------------------------------------------------
webui.buildWebui(config, logger, debugFlags)

