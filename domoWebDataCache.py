#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# Trying to define a data cache to store measurements
# (in a local structure, a file, a DB, ...)
#========================================================
import logging
from domoWebModule import domoWebModule
import datetime

logger = None
debugFlags = {}

#--------------------------------------------------------
# The high level cache class
#--------------------------------------------------------
class domoWebDataCache(domoWebModule) :
   def __init__(self, name) :
      domoWebModule.__init__(self, name)

   def cacheData(self, data) :
      pass

   def getData(self, n = 0 ):
      pass
  
#--------------------------------------------------------
# A circular RAM cache
#--------------------------------------------------------
class domoWebCircularDataCache(domoWebDataCache) :
   def __init__(self, name, size) :
      domoWebDataCache.__init__(self, name)
      self.data = [None]*size
      self.timestamps = [None]*size
      self.nbEntry = 0
      self.size = size
      
   def cacheData(self, data) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache] " + str(self.nbEntry) + " / " + str(self.size)+ " <- "+str(data))
      if (self.nbEntry < self.size) :
         self.data = self.data[0:min(self.nbEntry, self.size)] + [data]
         self.timestamps = self.timestamps[0:min(self.nbEntry, self.size)] + [int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()*1000)]
         self.nbEntry = self.nbEntry +1
      else :
         self.data = self.data[1:self.size] + [data]
         self.timestamps = self.timestamps[1:self.size] + [int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()*1000)]

   # Produce the n?n:nbEntry last records
   def getData(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getData] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      return self.data[0:min(self.nbEntry, n)]

   def getTimeStamps(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getTimeStamps] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      return self.timestamps[0:min(self.nbEntry, n)]

   # Produce the n?n:nbEntry last records
   def getTimeStampedData(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getData] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      return zip(self.timestamps[0:min(self.nbEntry, n)], self.data[0:min(self.nbEntry, n)])
   
   # Produce the mean on n?n:nbEntry last records
   def getMean(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getMean] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      if ( n > 0 ):
         return sum(self.data[0:min(self.nbEntry, n)]) / float(n)
      else :
         return 0.0
   
   # Produce the min of n?n:nbEntry last records
   def getMin(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getMin] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      print " *** Min OUT"
      return min(self.data[0:min(self.nbEntry, n)])

   # Produce the max of n?n:nbEntry last records
   def getMax(self, n=0) :
      if (('cacheVerbose' in debugFlags) or ('all' in debugFlags)) :
         logger.info("[cache.getMax] " + str(self.nbEntry) + " / " + str(self.size))
      if ( n == 0 ) :
         n = self.nbEntry
      return max(self.data[0:min(self.nbEntry, n)])

#--------------------------------------------------------
# Module init
#--------------------------------------------------------
def domoWebDataCacheInit(c, l, d) :
   logger = l
   debugFlags = d
   print"111111111111111111111111111"
   if (('cache' in debugFlags) or ('all' in debugFlags)):
      logger.debug("Initializing domoWebDataCache subsystem")
      print"222222222222222222222222"
   print"3333333333333331"

   
