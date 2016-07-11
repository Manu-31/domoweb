#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# Trying to define a data cache to store measurements
# (in a local structure, a file, a DB, ...)
#========================================================
import logging

#--------------------------------------------------------
# The high level cache class
#--------------------------------------------------------
class domoWebDataCache :
   def __init__(self) :
      pass

   def cacheData(self, data) :
      pass

   def getData(self, n = 0 ):
      pass
  
#--------------------------------------------------------
# A circular RAM cache
#--------------------------------------------------------
class domoWebCircularDataCache(domoWebDataCache) :
   def __init__(self, size) :
      domoWebDataCache.__init__(self)
      self.data = [None]*size
      self.nbEntry = 0
      self.size = size
      
   def cacheData(self, data) :
      self.nbEntry = self.nbEntry +1
      print "[cache] " + str(self.nbEntry) + " / " + str(self.size)
      self.data = [data] + self.data[0:min(self.nbEntry-2, self.size-1)]

   def getData(self, n=0) :
      print "[cache.getData] " + str(self.nbEntry) + " / " + str(self.size)
      if ( n == 0 ) :
         n = self.nbEntry
      return self.data[0:min(self.nbEntry, n)]
  
#--------------------------------------------------------
# Module init
#--------------------------------------------------------
def domoWebDataCacheInit(l) :
   global logger
   logger = l
   logger.info("Initializing domoWebDataCache ...")
   
