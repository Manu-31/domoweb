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
# . html             to be rendered
# . templateData()   to tune the html before rendering
# . setOptions()     to set some options (eg based on a config file)
# . update()         set parameters based on a dict
#=============================================================
class domoWebModule(object) :
   # We need to keep trace of the modules that have been defined
   domoWebModules = []
   actions = []
   debugFlags = {}
   
   # The constructor *must* be called by any subclass constructor
   def __init__(self, name, html="error.html") :
      self.logger = logging.getLogger('domoweb')

      # List of attributes that may be used in domoWeb. Warning : any
      # attribute CAN be used. Only domoWebAttributes will be shown in
      # automatic listings
      self.domoWebAttributes = []

      # Several modules with the same name is a bad idea !
      if (len([x for x in domoWebModule.domoWebModules if x.name == name]) != 0) :
         debug("module "+name+" defined twice !!!")
      
      self.name = name
      self.turnAttribute('name')

      self.html = html
      self.turnAttribute('html')

      self.addAttribute('hidden', True) # Par défaut, on ne montre pas

      # Là, c'est un peu tricky, ...
      self.addAttribute('readAccess', "")
      self.addAttribute('writeAccess', "")

      print "***** ATTENTION DROITS PAR DEFAUT A REVOIR *****"
      self.readUsers = None #[ User.get("all") ]
      self.writeUsers = None #[ adminUser ]

      domoWebModule.domoWebModules.append(self)
      if ('objectCreation' in domoWebModule.debugFlags) :
         self.logger.debug("Module '"+name+"' created")


   # Update some data from a dict (should be overridden)
   def update(self, dataDict):
      for name in dataDict :
         print self.name + "."+ name + " <- "+dataDict[name]
         self.setAttribute(name, dataDict[name])

   # Build a dictionary with local parameters
   # This dictionary will be used to display the web page
   # for the module. 
   def templateData(self):
      print "              HA ! TU VOIS QUE JE SERS A QUELQUE CHOSE  !!!"
      exit
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

   #=========================================================
   # Gestion des attributs
   #=========================================================
   # Add an attribute
   def addAttribute(self, attrName, attrValue) :
      if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
         self.logger.debug(self.name+"."+"addAttribute("+attrName+", <value>)")
      # We do not update existing non domoWeb attributes. Use
      # turnAttribute first
      if (not hasattr(self, attrName)):
         if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
            self.logger.debug("   (new attribute)")
         setattr(self, attrName, attrValue)
         # Register this attribute
         self.domoWebAttributes.append(attrName)
      else :
         if attrName in self.getAttributes() :
            if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
               self.logger.info("   (updated)")
            setattr(self, attrName, attrValue)
         else :
            if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
               self.logger.debug("   (unset)")
      if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
         self.logger.debug(self.name+"."+"addAttribute("+attrName+") done")

   # Turn a pre-defined python attribute into a DomoWeb one
   def turnAttribute(self, attrName) :
      if (attrName not in self.getAttributes()) :
         self.domoWebAttributes.append(attrName) 

   # Set an attribute value. should use mod.attr = val with a setter
   def setAttribute(self, attr, val) :
      print "     **** ATTENTION, ON DOIT VERIFIER EXISTENCE ET DROIT !! *** "
      print "     **** ET ON DOIT ENREGISTRER CA DANS LE LIVRE DE BORD!! *** "
      setattr(self, attr, val)
      

   # Get attribute list
   def getAttributes(self) :
      return self.domoWebAttributes

   # Get an attribute value
   def getAttribute(self, attr) :
      if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
         self.logger.info("getAttribute('"+self.name+"', '"+attr+"')")
                     
      # WARNING : should we check readAccess ?
      if (attr in self.getAttributes()) :
         if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
            self.logger.info("getAttribute : got it !")
         return getattr(self, attr, None)
      else :
         if (('objectAttributes' in domoWebModule.debugFlags) or ('all' in domoWebModule.debugFlags)) :
            self.logger.info("getAttribute : unknown !")
         
         return None

   def name(self):
      return self.name

   #-------------------------------------------------------------
   # User permissions
   #-------------------------------------------------------------
   # Access lists have a special reader/setter because internal
   # properties are named readUsers and writeUsers and are user
   # lists. The available versions are called readaccess and
   # writeaccess and are name lists, ...
   @property
   def readAccess(self):
      if (self.readUsers is None) :
         result = "*"
      else :
         if not self.readUsers :
            result = "None"
         else :
            result = ""
            for u in self.readUsers :
               result = result+" "+u.name()
      if ('users' in domoWebModule.debugFlags) :
         self.logger.debug("Reading readUsers for "+self.name+" : "+result)
      return result

   @readAccess.setter
   def readAccess(self, ral):
      if ('users' in domoWebModule.debugFlags) :
         self.logger.debug("Setting readUsers for '"+self.name +"' : "+ral)
      if (ral == "*") :
         self.setReadUsers(None)
      else :
         for u in string.split(ral, ',') :
            self.addReadUser(User.get(u))

   @property
   def writeAccess(self):
      if ('users' in domoWebModule.debugFlags) :
         self.logger.debug("Reading writeUsers for "+self.name+" : ")
         if (self.writeUsers is None) :
            print "PERSONNE"
         else :
            for u in self.writeUsers :
               print "   * "+u.name()
         self.logger.debug(self.writeUsers)
      return self.writeUsers

   @writeAccess.setter
   def writeAccess(self, ral):
      if ('users' in domoWebModule.debugFlags) :
         self.logger.debug("Setting writeUsers for '"+self.name +"' : "+ral)
      if (ral == "*") :
         self.setWriteUsers(None)
      else :
         for u in string.split(ral, ',') :
            self.addWriteUser(User.get(u))

   # set the reader list
   def setReadUsers(self, userList) :
      self.readUsers = userList
   
   # Add a single reader
   def addReadUser(self, user) :
      if (getattr(self, 'readUsers', None) is None) :
         self.readUsers = []
      if (user is not None): 
         self.readUsers.append(user)
 
   # Is user allowed to read data from this module ?
   def userCanRead(self, user) :
      allUser=User.get('all')
      return ((self.readUsers is None) or (((user in self.readUsers) or (allUser in self.readUsers)) and (user.is_authenticated)))

   # set the writer list
   def setWriteUsers(self, userList) :
      self.writeUsers = userList
   
   # Add a single writer
   def addWriteUser(self, user) :
      if (getattr(self, 'writeUsers', None) is None) :
         self.writeUsers = []
      if (user is not None): 
         if ('users' in domoWebModule.debugFlags) :
            self.logger.debug(self.name+".addWriteUser("+user.name()+")")
         self.writeUsers.append(user)
 
   # Is user allowed to read data from this module ?
   def userCanWrite(self, user) :
      allUser=User.get('all')
      return ((self.writeUsers is None) or (((user in self.writeUsers) or (allUser in self.writeUsers)) and (user.is_authenticated)))


   #-------------------------------------------------------------
   # The hidden property also deserves a special setter that could
   # be called with as string as well as a boolean
   #-------------------------------------------------------------
   @property
   def hidden(self):
      return self._hidden

   @hidden.setter
   def hidden(self, hide):
      self._hidden = ((hide == True) or (hide == 'True'))         
      

#-------------------------------------------------------------
# Retrieve module by name
#-------------------------------------------------------------
def getDomoWebModuleByName(name) :

#   print "getDomoWebModuleByName("+name+"), known modules :"
#   for x in domoWebModule.domoWebModules :
#      print "  - "+x.name

   for x in domoWebModule.domoWebModules :
      if x.name == name :
         return x
   return None

#-------------------------------------------------------------
#
#-------------------------------------------------------------
def domoWebModuleAction(func):
   print("domoWebModuleAction 1")
   print func

   def action(self) :
      print("Running Action "+func.__name__)
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
        self.setLevel(logging.NOTSET)
        self.setFormatter(formatter)
        logger = logging.getLogger('domoweb')
        logger.addHandler(self)

    def emit(self, record):
       self.messages.append({'ln' :record.levelname, 'st' : self.format(record)})
 
    def get_messages(self):
        return self.messages

# Le handler de logging
log_handler = webPageHandler()

#=============================================================
# A basic module : a debug page
#=============================================================
class debug(domoWebModule) :
   def __init__(self, name) :
      domoWebModule.__init__(self, name)
      self.html = "debug.html"
      #self.addReadUser(User.get("admin"))

#-------------------------------------------------------------
# The debugger page helper
#-------------------------------------------------------------
   def templateData(self):
      messages = []
      templateData = {}

      # WARNING : à faire, un paramètre qui définit les level à
      # afficher !
      for message in log_handler.get_messages()  :
         messages.append(message['st'])
         templateData['messages'] = messages

      return templateData

#=============================================================
# A basic module : a help page
#=============================================================
class help(domoWebModule) :
   def __init__(self, name) :
      domoWebModule.__init__(self, name)
      self.html = "help.html"
      self.readUsers = None # Everyone deserve some help !
      
#=============================================================
# A generic module : include a web page
#=============================================================
class embed(domoWebModule) :
   def __init__(self, name) :
      domoWebModule.__init__(self, name)
      self.html = "iframe.html"

   def templateData(self):
      templateData = {}
      templateData['url'] = self.url

      return templateData













