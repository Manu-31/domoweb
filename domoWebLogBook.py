#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#=============================================================
# The logbook is used to keep track of main events in domoWeb
#
# Events are represented as strings. Each event is timestamped by the
# loogBook.
#=============================================================
eventList = []

# Append a new event at the end of the list
def logBookAddEvent(eventDescription) :
   eventList.append((1, eventDescription))
   if (('logBook' in debugFlags) or ('all' in debugFlags)) :
      logger.debug("Event '"+eventDescription+"' appended to the logbook")
   
def logBookInit(config, l, df) :
   global debugFlags
   global logger

   debugFlags = df
   logger = l
   
   if (('logBook' in debugFlags) or ('all' in debugFlags)) :
      logger.debug("logBook initialized")
