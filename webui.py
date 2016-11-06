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
import types
import logging
import json

# Import available modules
from domoWebModule import *
from aquarium import *
from piscine import *
from domoWebSignIn import *

#=============================================================
# Les variables globales
#=============================================================

# Le web
app = Flask(__name__)


@app.route("/")
#@login_required
def accueil():
   return redirect(url_for('menu', module='aide'))

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
# This one gives value for remote display
#-------------------------------------------------------------
@app.route("/json/<module>/<value>")
#@login_required
def readValue(module, value):
   # Searching the module
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == module]
   # WARNING : r could be empty 
   choice = r[0]

   values = choice.templateData()
   if (not (value in values)) :
      logger.debug("Unkonwn value '"+value+"' for module "+module)

   print "*** Will return " + str(values[value])

   return Response(json.dumps(values[value]),mimetype='application/json')

#-------------------------------------------------------------
# Here is the route to access the defined modules
#-------------------------------------------------------------
@app.route("/menu/<module>", methods=['GET', 'POST'])
#@login_required
def menu(module):
   global logger
   
   # Searching the module
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == module]
   # WARNING : r could be empty 
   choice = r[0]

   # Data update from the user
   if request.method == 'POST':
      if (choice.userCanWrite(current_user)) :
         # Applying the update on the module
         choice.update(request.form)

         tabList = []
         for mod in domoWebModule.domoWebModule.domoWebModules :
            if mod.userCanRead(current_user)  :
               tabList.append(mod)
         templateData = {
            'tabList' :  tabList,
            'currentMenu' : module
         }

         # Updating displayed data
         templateData.update(choice.templateData())
 
         # Rendering the page
         logger.info("Rendering "+ choice.html +" for module "+choice.name)
         return render_template(choice.html, **templateData)
      else :
         return render_template("login.html", error="Vous n'avez pas les droits suffisants")
   
   # Data display
   else :
      if (choice.userCanRead(current_user)) :
         tabList = []
         for mod in domoWebModule.domoWebModule.domoWebModules :
            if mod.userCanRead(current_user)  :
               tabList.append(mod)
         templateData = {
            'tabList' :  tabList,
            'currentMenu' : module
         }
         templateData.update(choice.templateData())
         notification = request.args.get('notification', '')
         # Rendering the pagea
         logger.info("Rendering "+ choice.html +" for module "+choice.name)
         if (notification is None) :
            return render_template(choice.html, **templateData)
         else :
            return render_template(choice.html, notification=notification, **templateData)
      else :
         return render_template("login.html", error="Vous n'avez pas les droits suffisants")
         

@app.route('/menu/pouet', methods=['GET', 'POST'])
def pouet():
   templateData = {
      'tabList' :  domoWebModule.domoWebModule.domoWebModules,
      'currentMenu' : 'login'
   }

   # Searching the module
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == 'login']
   # WARNING : r could be empty 
   choice = r[0]

   error = None
   if request.method == 'POST':
      User("Manu", "manu")
      User("Admin", "admin")
      print "On cherche " + request.form['username']
      user = User.get( request.form['username'])
      choice.update(request.form)
      if (user is None) :
         print "Iconnu ..."
      else:
         print "On connait : "+user.id+"/"+user.password
         print user
         if (user.password == request.form['password']) :
            print "OK on log"
            login_user(user)
            print "Et on ouvre la page"
            print current_user
            return redirect(url_for('menu', module='aide'))
         else :
            error = 'Invalid Credentials. Please try again.'
           
   return render_template('login.html', error=error, **templateData)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('menu', module='aide'))

#-------------------------------------------------------------
# Run an action on a module
#-------------------------------------------------------------
@app.route("/do/<module>/<action>")
#@login_required
def do(module, action):
   print "Module"
   print module
   print "Action"
   print action

   # Searching the module
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == module]
   # WARNING : r could be empty 
   choice = r[0]

   print "Le choix est "
   print choice.name
   
   print "Les actions sont"
   print choice.__class__.actions

   if (hasattr(choice, action)) :
      print "** " + action + " est connue"
      actionFunc = getattr(choice, action)
      print actionFunc
      getattr(choice, action)()
      
      if (hasattr(actionFunc, "isAModuleAction")) :
         print "** C'est une action"
      else :
         print "** C'est PAS une action mon cochon"
         print vars(actionFunc)
         
   if (action in choice.__class__.actions) :
      print "+++++++++++ Connue"
      # Is the user allowed to run an action on this module ?
      if (choice.userCanWrite(current_user)) :
         # Searching and calling the corresponding action
         getattr(choice, action)()

         return redirect(url_for("menu", module=module, notification="C'est fait"))
      else :
         return redirect(url_for("menu", module=module, notification="Forbidden"))
   else :
      print("Action "+ module + "." + action +  " inconnue")
      logger.debug("Action "+ module + "." + action +  " inconnue")
      return redirect(url_for("menu", module=module, notification="Erreur interne"))

#-------------------------------------------------------------
# List all available data
#-------------------------------------------------------------
@app.route("/list")
#@login_required
def listParameters():
   moduleList = []
   
   for x in domoWebModule.domoWebModule.domoWebModules :
      newMod = {'name' : x.name, 'actions' : [], 'module' : []}
      td = x.templateData()
      for n in td :
         print "------------------"
         print n
         print td[n]
         print "------------------"
         newMod['module'].append({'name' : n, 'v' : td[n]})
      for a in x.__class__.actions :
         newMod['actions'].append(a)
      moduleList.append(newMod)

   return render_template('datalist.html',  moduleList=moduleList)

def strToClass(s):
   if s in globals() and isinstance(globals()[s], types.ClassType):
      return globals()[s]
   return None

#=============================================================
# Build the webui from config file
#=============================================================
def buildWebui(config):
   global logger
   logger = logging.getLogger('domoweb')

   # Create users : admin and the one defined in config
   adminUser = User("admin", "admin")
   tabList = config.items('users')
   for login, desc in tabList :
      lines = string.split(desc, ":")
      User(login, lines[0])

   # Create tabs
   tabList = config.items('tabs')
   for modName, modType in tabList :
      logger.info("Loading tab " + modName + " (type " + modType +")")
      
      # Retrieve the module class
      domoWebModuleClass = strToClass(modType)
      
      # Create the object 
      domoModule = domoWebModuleClass(modName)

      # Set as public [WARNING]
      domoModule.setReadUsers(None)
      
      # Set options from the config
      if (config.has_section(modName)) :
         domoModule.setOptions(config.items(modName))

#-------------------------------------------------------------
# Run the web server
#-------------------------------------------------------------
   logger.info("Lancement du serveur web")
   app.config["SECRET_KEY"] = "CaCestUnPunaiseDeSecret"
   app.run(host='0.0.0.0', port=8081, debug=False)
  

