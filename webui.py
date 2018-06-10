#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
# Gestion de l'interface web de mes petits jouets domotifiants
#
# La notion de base est le domoWebModule. Un tel module
# définit un type d'objet pouvant être géré par domoWeb.
# La seconde notion est le domoWebTab. Un domoWebTab est une
# interface dédiée à un objet réel. Un domoWebTab est caractérisé
# en particulier par le domoWebModule qui l'implante.
#-------------------------------------------------------------
# To be done
#
# 0.03
#   Formatted output on the debug page
#   Interactive page : select messages shown in the debug page
#
#=============================================================

from flask import Flask, url_for, render_template, redirect, Response, request
from flask_login import \
   LoginManager, UserMixin, \
   login_required, login_user, logout_user, current_user

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import types
import logging
import json

# Import available modules
from domoWebModule import *
from domoWebModule import domoWebModule as generic
#from aquarium import *
#from piscine import *
from domoWebSignIn import *
from oneWireDevice import *
from gpioDevice import *

#=============================================================
# Les variables globales
#=============================================================

# Le web
app = Flask(__name__)

# Le debug flag
debugFlags = {}

@app.route("/")
#@login_required
def accueil():
   return redirect(url_for('menu', modName='aide'))

#=============================================================
# Gestion de l'authentification
#=============================================================
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


#=============================================================
# Some helper functions
#=============================================================
   
#-------------------------------------------------------------
# Creation of the menu list based on the selected module, connected
# user, ...
# Input
#    module      : selected module
# This function returns a templateData with data for the generic
# header (with the menu)
#    tabList     : list of available modules
#    module      : the current selected module
#-------------------------------------------------------------
def menuTemplateData(module) :
   return

#=============================================================
# Definition of the routes.
#=============================================================
#-------------------------------------------------------------
# This one gives value for remote display
#-------------------------------------------------------------
@app.route("/json/<modName>/<value>")
#@login_required
def readValue(modName, value):
   # Searching the module WARNING : module could be None
   module = getDomoWebModuleByName(modName)
   
   values = module.templateData()
   if (not (value in values)) :
      logger.debug("Unkonwn value '"+value+"' for module "+module.name)

   print "*** Will return " + str(values[value])

   return Response(json.dumps(values[value]),mimetype='application/json')

#-------------------------------------------------------------
# Here is the route to access the defined modules
#-------------------------------------------------------------
@app.route("/menu/<modName>", methods=['GET', 'POST'])
#@login_required
def menu(modName):
   global logger

   # Searching the module WARNING : module could be None
   module = getDomoWebModuleByName(modName)

   # Data update from the user
   if request.method == 'POST':
      if (module.userCanWrite(current_user)) :
         # Applying the update on the module
         module.update(request.form)

         tabList = []
         for mod in domoWebModule.domoWebModules :
            logger.debug(mod.name + " is hidden ? ")
            logger.debug(str(mod.hidden))
            if ((mod.hidden == False) and (mod.userCanRead(current_user)))  :
               tabList.append(mod)
         templateData = {
            'tabList' :  tabList,
            'module'  : module
         }

         # Updating displayed data
         templateData.update(module.templateData())
 
         # Rendering the page
         logger.info("Rendering "+ module.html +" for module "+module.name)
         return render_template(module.html, **templateData)
      else :
         return render_template("login.html", error="Vous n'avez pas les droits suffisants")
   
   # Data display
   else :
      if (module.userCanRead(current_user)) :

         # Build tabList for main menu
         #----------------------------
         tabList = []
         if (current_user.is_authenticated) :
            cuName = current_user.name()
         else :
            cuName = "Unkonwn"

         for mod in domoWebModule.domoWebModules :
            if ('permissions' in debugFlags) :
               logger.debug("Can we show '"+mod.name+"' to current user ('"+cuName+"') ?")
               logger.debug("     hidden    = "+str(mod.hidden))
               logger.debug("     readUsers = "+ mod.readaccess)
            if ((mod.hidden == False) and mod.userCanRead(current_user))  :
               if ('permissions' in debugFlags) :
                  logger.debug("Yes, we can !")
               tabList.append(mod)
            else :
               if ('permissions' in debugFlags) :
                  logger.debug("No, we can't !")
         #############################
         
         templateData = {
            'tabList' :  tabList,
            'module'  : module
         }

         templateData.update(module.templateData())
         notification = request.args.get('notification', '')

         # Rendering the page
         logger.info("Rendering "+ module.html +" for module "+module.name)
         if (notification is None) :
            return render_template(module.html, **templateData)
         else :
            return render_template(module.html, notification=notification, **templateData)
      else :
         return render_template("login.html", error="Vous n'avez pas les droits suffisants")
         
#-------------------------------------------------------------
# Encore un essai, ...
#-------------------------------------------------------------
@app.route("/<modName>/<attribute>/<value>")
#@login_required
def setModuleParameter(modName, attribute, value):
   print "Dans le module "+modName
   print "   L'attribut  "+ attribute
   print "        reçoit "+value

#-------------------------------------------------------------
# Run an action on a module.
# . modName is the name of the module
# . action is the action to run (modName.action() )
# . destModule, if present, is the name of the module to display
#   (eg if module is a switch, you may want to display the
#   switch parent)
#-------------------------------------------------------------
@app.route("/do/<modName>/<action>")
@app.route("/do/<modName>/<action>/<destModule>")
#@login_required
def do(modName, action,destModule=""):

   # Searching the module WARNING : module could be None
   module = getDomoWebModuleByName(modName)

   if not destModule :
      destModule=modName
      
   print "%%% Destination : '"+destModule+"'"
   
   if ('actions' in debugFlags) :
      logger.debug("Trying to run action '"+action+"' on '"+modName+"' (class '"+module.__class__.__name__+"')")
   
   print "Les actions sont"
   print module.__class__.actions

   if (hasattr(module, action)) :
      print "** " + action + " est connue"
      actionFunc = getattr(module, action)
      print actionFunc
      getattr(module, action)()
      
      if (hasattr(actionFunc, "isAModuleAction")) :
         print "** C'est une action"
      else :
         print "** C'est PAS une action mon cochon"
         print vars(actionFunc)
         
   if (action in module.__class__.actions) :
      # Is the user allowed to run an action on this module ?
      if (module.userCanWrite(current_user)) :
         # Searching and calling the corresponding action
         getattr(module, action)()

         return redirect(url_for("menu", modName=destModule, notification="C'est fait"))
      else :
         return redirect(url_for("menu", modName=destModule, notification="Forbidden"))
   else :
      print("Action "+ module + "." + action +  " inconnue")
      logger.debug("Action "+ module + "." + action +  " inconnue")
      return redirect(url_for("menu", modName=module.name, notification="Erreur interne"))

#-------------------------------------------------------------
# List all available data
#-------------------------------------------------------------
@app.route("/list")
#@login_required
def listParameters():
   moduleList = []
   hiddenList = []

   logger.debug("Module list : ")
 
   for x in domoWebModule.domoWebModules :
      if (getattr(x, 'hidden') == False) :
         moduleList.append(x)
         logger.debug("- '" + x.name + "' (public) with the following attributes")
      else :
         hiddenList.append(x)
         logger.debug("- '" + x.name + "' (hidden) with the following attributes")
      for a in x.getAttributes() :
            logger.debug("  . "+ a)

   logger.debug("End of module list")

   return render_template("datalist.html", moduleList=moduleList, hiddenList=hiddenList)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('menu', modName='aide'))

def strToClass(s):
   if s in globals() and issubclass(globals()[s], domoWebModule):
      return globals()[s]
   return None

#=============================================================
# WARNING : the following functions should be ... elsewhere
#=============================================================
# Create a domoWebModule named name with value, where value can
# be one of the following :
#
#   (1) value = previously_defined_name
#   (2) value = attrType,attrParam
#   (3) value = arbitrary string
#
#   where
#
#   attrType : actual class of the module
#   attrParam : parameter list
#
def stringToDomoWebModule(name, value) :
   attrParam = string.split(value, ",")
   attrType = attrParam.pop(0)

   # if the first list element is the name of a predefined module
   # (1) case "value = previously_defined_name"
   predefAttr = getDomoWebModuleByName(attrType)
   if (predefAttr is not None) :
      if ('objectCreation' in debugFlags) :
         logger.debug("stringToDomoWebModule : '"+attrType+"' already defined")
      return predefAttr     

   # (3) case "value = arbitrary string"
   attrCls = strToClass(attrType)
   if (attrCls is None) :
      if ('objectCreation' in debugFlags) :
         logger.debug("stringToDomoWebModule '"+value+"' is a string" );
      result = value # eg strings

   # Is this a new module declaration ?
   # (2) case "value = attrType,attrParam"
   else :
      if ('objectCreation' in debugFlags) :
         logger.debug("Création d'un '"+attrType+"' avec comme param :");
         logger.debug(attrParam)
      result = attrCls(name, l=attrParam)
   return result

# Create objects from an option list and add these attributes to a
# domoWebModule 
def addAttributes(dwm, optionList):
   ol = list(optionList)
   for name, value in ol :
      if ('objectCreation' in debugFlags) :
         logger.debug("addAttributes : "+dwm.name+" reçoit un attribut '"+ name+"' de valeur '"+value+"'")

      # Create a module
      attr=stringToDomoWebModule(dwm.name+"."+name, value)

      # Add this as an attribute
      dwm.addAttribute(name, attr)
      
      del optionList[optionList.index((name, value))]


#-------------------------------------------------------------
# Creation of multiple modules described in a section of the config
# file. Such a section is a list of
#
# name = type[,options]
#
# where type is a subclass of domoWebModule
#-------------------------------------------------------------
def createModulesFromSection(config, sectionName, hidden) :
   tabList = config.items(sectionName)
   for modName, optionList in tabList :
      if ('objectCreation' in debugFlags) :
         logger.debug("createModulesFromSection : " + modName + " (type " + optionList +")")
      domoModule = stringToDomoWebModule(modName, optionList)

      if hidden :
         domoModule.addAttribute('hidden', True)
      else :
         domoModule.addAttribute('hidden', False)
         
      # Set as public [WARNING]
      domoModule.setReadUsers(None)
      
      # Set options from the config
      if (config.has_section(modName)) :
         if ('objectCreation' in debugFlags) :
            logger.debug("Loading parameters for' " + modName + "'")
         addAttributes(domoModule, config.items(modName))

            
#=============================================================
# Build the webui from config file
#=============================================================
def buildWebui(config, l,  dbgFlg) :
   global debugFlags
   global logger
   
   debugFlags = dbgFlg

   logger = l # ou alors logger = logging.getLogger('domoweb')

   # Create users : admin and the one defined in config
   if ('users' in debugFlags) :
      logger.debug("-- User creation ...")
   adminUser = User("admin", "admin")
   tabList = config.items('users')
   for login, desc in tabList :
      lines = string.split(desc, ":")
      User(login, lines[0])

   # Create hidden modules
   if ('objectCreation' in debugFlags) :
      logger.debug("-- Hidden modules creation ...")
      logger.debug("------------------------------")
   createModulesFromSection(config, 'modules', True)
   
   # Create tabs
   if ('objectCreation' in debugFlags) :
      logger.debug("-- Public modules creation ...")   
      logger.debug("------------------------------")   
   createModulesFromSection(config, 'tabs', False)   

#-------------------------------------------------------------
# Run the web server
#-------------------------------------------------------------
   logger.info("Lancement du serveur web")
   app.config["SECRET_KEY"] = "CaCestUnPunaiseDeSecret"
   app.run(host='0.0.0.0', port=8081, debug=False)
  

