#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Definition and manipulation of domoWebModules plus some
# basic modules.
#
#=============================================================
import string
import logging
from domoWebUser import *

def printUserList(l) :
   if (l is None) :
      print ("*")
   else :
      print "(SOL)"
      for u in l :
         print u.name() + " "
      print "(EOL)"

#=============================================================
# A domoWebModule is characterized by
# . name
# . title            to be displayed
# . html             to be rendered
# . templateData()   to tune the html before rendering
# . setOptions()     to set some options (eg based on a config file)
# . update()         set parameters based on a dict
#=============================================================
class domoWebModule :
   # We need to keep trace of the modules that have been defined
   domoWebModules = []
   actions = []

   # The constructor *must* be called by any subclass constructor
   def __init__(self, name, html="error.html"):
      if (len([x for x in domoWebModule.domoWebModules if x.name == name]) != 0) :
         debug("module "+name+" defined twice !!!")
      self.attributes = []
      self.setName(name)
      self.setTitle(name)
      self.setHtml(html)
      self.readUsers = []
      self.writeUsers = []
      domoWebModule.domoWebModules.append(self)

   # Add an attribute
   def addAttribute(self, dwAttr) :
      self.attributes.append(dwAttr)

   def setOptions(self, optionList):
      ol = list(optionList)
      for name, value in ol :
         print self.name + "."+ name + " = "+value

         if (name == "html") :
            self.setHtml(value)
            del optionList[optionList.index((name, value))]

         # Dealing with permissions
         if (name == 'readaccess') :
            if (value == "*") :
               self.setReadUsers(None)
            else :
               for u in string.split(value, ',') :
                  self.addReadUser(User.get(u))
            del optionList[optionList.index((name, value))]

         if (name == 'writeaccess') :
            if (value == "*") :
               self.setWriteUsers(None)
            else :
               for u in string.split(value, ',') :
                  self.addWriteUser(User.get(u))
            del optionList[optionList.index((name, value))]

   # Update some data from a dict (should be overridden)
   def update(self, dataDict):
      for name in dataDict :
         print self.name + "."+ name + " <- "+dataDict[name]

         #WARNING: SHOULD WE SET ANY ATTRIBUTE ? 
         #setattr(self, name, value)

   def setName(self, name):
      self.name =  name
      self.addAttribute(self.name) 

   def setTitle(self, title):
      self.title = title
      self.addAttribute(self.title) 

   def setHtml(self, html) :
      self.html = html
      self.addAttribute(self.html)

   # Build a dictionary with local parameters
   # This dictionary will be used to display the web page
   # for the module. 
   def templateData(self):
      templateData = {} #{'domoWebModuleName' : self.name}

      # Searching attributes
      for a in vars(self) :
         b = getattr(self, a)
         if (hasattr(b, "isADomoWebModuleAttribute")) :
            templateData[a] = b.getValue()

            print "["+a+"] est un attribut de "+self.name
            print "Valeur de a : "
            print b.getValue()
            
      return templateData

   # Get attribute list
   def getAttributes(self) :
      return self.attributes

   def name(self):
      return self.name

#-------------------------------------------------------------
# User permissions
#-------------------------------------------------------------
   # set the reader list
   def setReadUsers(self, userList) :
      self.readUsers = userList
   
   # Add a single reader
   def addReadUser(self, user) :
      if (self.readUsers is None) :
         self.readUsers = []
      self.readUsers.append(user)
 
   # Is user allowed to read data from this module ?
   def userCanRead(self, user) :
      return ((self.readUsers is None) or ((user in self.readUsers) and (user.is_authenticated)))

   # set the writer list
   def setWriteUsers(self, userList) :
      self.writeUsers = userList
   
   # Add a single writer
   def addWriteUser(self, user) :
      if (self.writeUsers is None) :
         self.writeUsers = []
      self.writeUsers.append(user)
 
   # Is user allowed to read data from this module ?
   def userCanWrite(self, user) :
      return ((self.writeUsers is None) or ((user in self.writeUsers) and (user.is_authenticated)))

#-------------------------------------------------------------
#
#-------------------------------------------------------------
def domoWebModuleAction(func):
   print("domoWebModuleAction 1")
   print func
   
   def action(self) :
      print("domoWebModuleAction 2")
      return func(self)

   print("domoWebModuleAction 3")
   action.isAModuleAction = True
   print vars(action)

   return action

#-------------------------------------------------------------
#
#-------------------------------------------------------------
def domoWebModuleAttribute(func):
   print("domoWebModuleAttribute 1")
   print func
   
   def action(self) :
      print("domoWebModuleAttribute 2")
      return func(self)

   print("domoWebModuleAttribute 3")
   action.isAModuleAttribute = True
   print vars(action)

   return action

#-------------------------------------------------------------
# Pour pouvoir logguer sur une page web
# (from https://gist.github.com/jhorneman/3181165)
#-------------------------------------------------------------
class webPageHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.messages = []

        # Ajout d'un handler pour la page web
        formatter = logging.Formatter("<td>%(asctime)s </td><td> %(levelname)s </td><td>%(message)s</td>")
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

