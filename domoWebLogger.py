#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
# Logger ...
#=============================================================
import logging

logger = None
debugFlags = {}

#-------------------------------------------------------------
# Initialization of the logging facilities
#-------------------------------------------------------------
def domoWebLoggerInit(config) :
   global logger
   global debugFlags
   
#-------------------------------------------------------------
# Default debuging
#-------------------------------------------------------------
   logFileName = config.get('general', 'logFileName')
   logConsole  = config.getboolean('general', 'logConsole')
   debugFlags  = config.get('general', 'debugFlags')

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

   logger.info("DomoWeb logger running")

