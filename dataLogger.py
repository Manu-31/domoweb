#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
# Data logging facilities
#=============================================================

class dataLogger :
   def __init__(self):
      pass
   
   def logData(self, dataDict) :
      for data in dataDict :
         print "LOGGING " + data + " = " + str(dataDict[data])

class mySQLDataLogger(dataLogger) :
   def __init__(self):
      pass

    
