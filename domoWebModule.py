#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Definition and manipulation of domoWebModules plus some
# basic modules.
#
#=============================================================
import logging

#=============================================================
# A domoWebModule is characterized by
# . name
# . title            to be displayed
# . html             to be rendered
# . templateData()   to tune the html before rendering
#=============================================================
class domoWebModule :
   # We need to keep trace of the modules that have been defined
   domoWebModules = []
   actions = []

   # The constructor *must* be called by any subclass constructor
   def __init__(self, name, html="error.html"):
      if (len([x for x in domoWebModule.domoWebModules if x.name == name]) != 0) :
         debug("module "+name+" defined twice !!!")
      self.name = name
      self.title = name
      self.setHtml(html)
      domoWebModule.domoWebModules.append(self)

   def setOptions(self, optionList):
      for name, value in optionList :
         print self.name + "."+ name + " = "+value

         #WARNING: SHOULD WE SET ANY ATTRIBUTE ? 
         setattr(self, name, value)

   def setTitle(self, title):
      self.title = title

   def setHtml(self, html) :
      self.html = html

   def templateData(self):
      return {}

   def name(self):
      return self.name

#-------------------------------------------------------------
# Pour pouvoir logguer sur une page web
# (from https://gist.github.com/jhorneman/3181165)
#-------------------------------------------------------------
class webPageHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.messages = []

        # Ajout d'un handler pour la page web
        formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(message)s')
        self.setLevel(logging.INFO)
        self.setFormatter(formatter)
        logger = logging.getLogger('domoweb')
        logger.addHandler(self)

    def emit(self, record):
        self.messages.append(self.format(record))
 
    def get_messages(self):
        return self.messages

# Le handler de logging
log_handler = webPageHandler()

#=============================================================
# A basic module : a debug page
#=============================================================
class debug(domoWebModule) :
   def __init__(self, name, html="debug.html") :
      domoWebModule.__init__(self, name, html)

#-------------------------------------------------------------
# The debugger page helper
#-------------------------------------------------------------
   def templateData(self):
      messages = []
      templateData = {}

      for message in log_handler.get_messages()  :
         messages.append(message)
         templateData['messages'] = messages

      return templateData

#=============================================================
# A basic module : a help page
#=============================================================
class help(domoWebModule) :
   def __init__(self, name, html="help.html") :
      domoWebModule.__init__(self, name, html)

#=============================================================
# A generic module : include a web page
#=============================================================
class embed(domoWebModule) :
   def __init__(self, name, html="iframe.html") :
      domoWebModule.__init__(self, name, html)

   def templateData(self):
      templateData = {}
      templateData['url'] = self.url

      return templateData


