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
from wtforms import *

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
   templateData = {
      'tabList' :  domoWebModule.domoWebModule.domoWebModules
   }
   return render_template('help.html', **templateData)

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
#--------------------------------------------------------
# This one gives value for remote display
#--------------------------------------------------------
@app.route("/json/<module>/<value>")
#@login_required
def readValue(module, value):
   # Searching the item
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == module]
   # WARNING : r could be empty 
   choice = r[0]

   values = choice.templateData()
   if (not (value in values)) :
      logger.debug("Unkonwn value '"+value+"' for module "+module)

   print "*** Will return " + str(values[value])

   return Response(json.dumps(values[value]),mimetype='application/json')

#--------------------------------------------------------
# Here is the route to access the defined modules
#--------------------------------------------------------
@app.route("/menu/<item>", methods=['GET', 'POST'])
#@login_required
def menu(item):
   templateData = {
      'tabList' :  domoWebModule.domoWebModule.domoWebModules,
      'currentMenu' : item
   }

   # Searching the item
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == item]
   # WARNING : r could be empty 
   choice = r[0]

   if request.method == 'POST':
      choice.update(request.form)
   else :
      if (choice.userCanRead(current_user)) :
         templateData.update(choice.templateData())
      else :
         return render_template("login.html", error="Vous n'avez pas les droits suffisants")
         
   return render_template(choice.html, **templateData)

@app.route('/menu/pouet', methods=['GET', 'POST'])
def pouet():
   templateData = {
      'tabList' :  domoWebModule.domoWebModule.domoWebModules,
      'currentMenu' : 'login'
   }

   # Searching the item
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
            return redirect(url_for('menu', item='aide'))
         else :
            error = 'Invalid Credentials. Please try again.'
           
   return render_template('login.html', error=error, **templateData)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('menu', item='aide'))

@app.route("/do/<item>/<action>")
#@login_required
def do(item, action):
   print "Item"
   print item
   print "Action"
   print action

   # Searching the item
   r = [x for x in domoWebModule.domoWebModule.domoWebModules if x.name == item]
   # WARNING : r could be empty 
   choice = r[0]

   print "Le choix est "
   print choice.name
   
   print "Les actions sont"
   print choice.__class__.actions
  
   if (action in choice.__class__.actions) :
      print "Connue" 
      # Searching and calling the corresponding action
      getattr(choice, action)()
   
   return redirect(url_for("menu", item=item))

#-------------------------------------------------------------
# List all available data
#-------------------------------------------------------------
@app.route("/list")
#@login_required
def listParameters():
   moduleList = []
   
   for x in domoWebModule.domoWebModule.domoWebModules :
      newMod = {'name' : x.name, 'actions' : [], 'item' : []}
      td = x.templateData()
      for n in td :
         print "------------------"
         print n
         print td[n]
         print "------------------"
         newMod['item'].append({'name' : n, 'v' : td[n]})
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
  

