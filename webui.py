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
import datetime

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
# Definition of the routes.
#=============================================================

#-------------------------------------------------------------
# Root route
#-------------------------------------------------------------
@app.route("/")
#@login_required
def accueil():
   return redirect(url_for('menu', modName=defaultModule))

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
   # WARNING : chercher les attributs du module tab
   module = getDomoWebModuleByName(modName)

   # Build tabList for main menu
   tabList = []
   for mod in domoWebModule.domoWebModules :
      if ((mod.hidden == False) and mod.userCanRead(current_user))  :
         tabList.append(mod)

   # Build the template data
   templateData = {
      'templateTheme' : templateTheme,
      'tabList'       : tabList,
      'startOfDay'    : datetime.datetime.combine(datetime.date.today(), datetime.time())
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
# Build the webui
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
  

