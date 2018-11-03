#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# Trying to implement asynchronous task management in
# domoweb
#========================================================

import threading, Queue
import time, datetime
import logging

debugFlags = {}

# We use a priority queue where priority is the date
taskQueue = Queue.PriorityQueue()

# We will use an event to wait for new event
newTask = threading.Event()

def affiche(m) :
    print m
#========================================================
# Queue a task
#   dt is the datetime for the task (0 for now)
#   f  is a function to run
#   d  is some data to pass to f
#   p  is the timedelta for the period (0 for single shot)
#  So a time dt f(d) is ran
#========================================================
def queueTask(dt, f, d, p=0) :
   if ('taskVerbose' in debugFlags) :
       logger.info("New task dt="+str(dt)+" period "+str(p) + " data :" + str(d))
       
#   print "New task dt="+str(dt)+" period "+str(p) + " data :"
#   print d
   if (dt == 0) :
      dt = datetime.datetime.now() 
   if ('taskVerbose' in debugFlags) :
      logger.info("Queueing new event for "+dt.isoformat())

   taskQueue.put((dt, {'func' : f, 'data' : d, 'period' : p}))

   # Let's wake up the main thread (note : this will raise
   # some spurious wakeups, but never mind !)
   newTask.set()
   
#========================================================
# Main loop running tasks
#========================================================
def runTaskQueue() :
   if ('taskVerbose' in debugFlags) :
      logger.info("Starting to run task queue")
   while (1 == 1) :
      newTask.clear() # Warning, should be protected
      tsk = taskQueue.get(True)
      f = tsk[1]['func']
      d = tsk[1]['data']
      period = tsk[1]['period']
      
      # Is it time ?
      if (tsk[0] > datetime.datetime.now() + datetime.timedelta(seconds=2)) :
         # Let's requeue the event
         taskQueue.put(tsk)

         # We should sleep now ! But we will wait so that
         # we could be warned if a new (earlier) task is queued
         newTask.wait((tsk[0] - datetime.datetime.now()).total_seconds())
      elif (tsk[0] < datetime.datetime.now() - datetime.timedelta(seconds=2)) :
         #print "It's to late for "
         #print d
	 pass
      else :
         # Re queue periodic task
         if (period != 0) :
            queueTask(datetime.datetime.now()+period, f, d, period)

         # Actually running the task
         if ('taskVerbose' in debugFlags) :
            logger.info("Running task")
         f(d)

#========================================================
# Starting tasks
#========================================================
def domoTaskStart() :
   if ('task' in debugFlags) :
       logger.info("Running tasks")
   # These 3 tasks should be removed
   #queueTask(datetime.datetime.now() + datetime.timedelta(seconds=30), affiche, "Plus tard")
   #queueTask(0, affiche, "Maintenant")
   #queueTask(datetime.datetime.now(), affiche, "Periode", datetime.timedelta(seconds=5))

   mainThread = threading.Thread(target=runTaskQueue)
   mainThread.start()
    
#========================================================
# Subsystem initalization.
# No task is start yet, as some subsystems may not be ready
#========================================================
def domoTaskInit(l, dbgFlg) :
   global debugFlags
   global logger
   
   logger = l
   debugFlags = dbgFlg
   
   if ('task' in debugFlags) :
       logger.info("Initializing domoTask subsystem")

   
    
