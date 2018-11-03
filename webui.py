#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
# Management of a web user interface
#=============================================================

from flask import Flask, url_for, render_template, redirect, Response, \
request, session
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
from domoWebAction import domoWebAction

#=============================================================
# Les variables globales
#=============================================================

# Le web
app = Flask(__name__)

# Le theme (WARNING : à mettre un jour dans la session)
#templateTheme = "default"
#templateTheme = "echarts"
#templateTheme = "highcharts"
templateTheme = "chartist"

# Le debug flag
debugFlags = {}

# Default page
defaultModule = "aide"

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
# Root route
#-------------------------------------------------------------
@app.route("/")
#@login_required
def accueil():
   return redirect(url_for('menu', modName=defaultModule))

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

   if (('webui' in debugFlags) or ('all' in debugFlags)) :
      logger.debug("Requesting page /menu/"+modName+" (method "+request.method+")")

   # Searching the module 
   module = getDomoWebModuleByName(modName)

   # Build tabList for main menu
   tabList = []
   for mod in domoWebModule.domoWebModules :
      if ((mod.hidden == False) and mod.userCanRead(current_user))  :
         tabList.append(mod)

   # Build the template data
   templateData = {
      'templateTheme' : templateTheme,
      'tabList'       : tabList
   }
   notification = None
   error = None
   
   # An unknwon module is a bug, ...
   if (module is None) :
      if (('webui' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("Unknown module '"+modName+"'")
      # Return to default route
      template = "error.html"
      error = "Internal error ! Should not happen"
   else :
      template = module.html
      if (('webui' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("Module '"+modName+"' found")
         
      # Data update from the user
      if request.method == 'POST':
         if (('webui' in debugFlags) or ('all' in debugFlags)) :
            logger.debug("Updating module '"+mod.name+"' (POST method)")
      
         if (module.userCanWrite(current_user)) :
            # Applying the update on the module
            module.update(request.form)
            notification = "Successfully updated"
         else :
            error = "Won't do this : it's above your paygrade !"
         
      # Render the template (GET and POST)
      if (module.userCanRead(current_user)) :

         # Insert the module in the template data
         templateData.update( {
            'module'        : module
         })

         # Add template data from the module (WARNING : à virer)
         templateData.update(module.templateData())

         # WARNING : C'est quoi !?
         notification = request.args.get('notification', '')

      else :
         template="error.html"
         error="Can't show you that, ..."

   # Rendering the page
   if (('webui' in debugFlags) or ('all' in debugFlags)) :
      logger.info("Rendering "+ template +" ...")

   return render_template(template, notification=notification, error=error, **templateData)

         
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
   
   if (('actions' in debugFlags) or ('all' in debugFlags)) :
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
# Set attribute for a module
#-------------------------------------------------------------
@app.route("/setAttribute/<modName>/<attribute>/<value>")
@app.route("/setAttribute/<modName>/<attribute>/<value>/<destModule>")
def setAttribute(modName, attribute, value, destModule=""):
   if (('actions' in debugFlags) or ('webui' in debugFlags ) or ('all' in debugFlags)) :
      logger.debug("setAttribute("+ modName + ", " + attribute + ", " + value + ")")
      
   # Searching the module WARNING : module could be None
   module = getDomoWebModuleByName(modName)

   # WARNING : hardcoded default module
   if (module is None) :
      return redirect(url_for("menu", modName='aide', notification="Unknown module"))
      
   # If no destination module, we will render the first one
   if not destModule :
      destModule=modName

   # Now we have to check permissions
   if (module.userCanWrite(current_user)) :

      # Let us now try to set the attribute
      module.setAttribute(attribute, value)
      
      # Let us print some encouragement
      notif = attribute + " successfully updated !"
   else :
      # Let us print some encouragement
      notif = attribute + " is above your paygrade !"
   
   # Show the destination module plus a notification
   return redirect(url_for("menu", modName=destModule, notification=notif))
      

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

#=============================================================
# Build the webui from config file
#=============================================================
def buildWebui(config, l,  dbgFlg) :
   global debugFlags
   global logger
   
   debugFlags = dbgFlg

   logger = l # ou alors logger = logging.getLogger('domoweb')

   if (('webui' in debugFlags) or ('all' in debugFlags)) :
      logger.info("Building web UI")

#-------------------------------------------------------------
# Run the web server
#-------------------------------------------------------------
   webUIPort = 8081
   if (config.has_option('general', 'port')) :
      webUIPort = config.getint('general', 'port')

   print([cls.__name__ for cls in domoWebModule.__subclasses__()])

   if (('webui' in debugFlags) or ('all' in debugFlags)) :
      logger.info("Lancement du serveur web")
   app.config["SECRET_KEY"] = "CaCestUnPunaiseDeSecret"
   app.run(host='0.0.0.0', port=webUIPort, debug=False)
  

