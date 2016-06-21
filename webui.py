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
#   Header/footer data in the generic helper
#   Interactive page : select messages shown in the debug page
#
# ?.??
#   
#=============================================================
#webUIVersion = "0.00"          # First try
#webUIVersion = "0.01"          # Roughly usable
webUIVersion = "0.02"           # Modules as class

from flask import Flask, url_for, render_template, redirect, Response
import sys
import types
import logging
import json

from aquarium import *
from piscine import *
from domoWebModule import *

#=============================================================
# Les variables globales
#=============================================================

# Le web
app = Flask(__name__)

#=============================================================
# Definition of the routes.
#=============================================================
#--------------------------------------------------------
# This one gives value for remote display
#--------------------------------------------------------
@app.route("/json/<module>/<value>")
def readValue(module, value):
   # Searching the item
   r = [x for x in domoWebModule.domoWebModules if x.name == module]
   # WARNING : r could be empty 
   choice = r[0]

   values = choice.templateData()
   if (not (value in values)) :
      logger.debug("Unkonwn value '"+value+"' for module "+module)

   print "*** Will return " + str(values[value])

   return Response(json.dumps(values[value]),mimetype='application/json')

@app.route("/menu/<item>")
def menu(item):
   templateData = {
      'tabList' :  domoWebModule.domoWebModules,
      'currentMenu' : item
   }

   # Searching the item
   r = [x for x in domoWebModule.domoWebModules if x.name == item]
   # WARNING : r could be empty 
   choice = r[0]

   templateData.update(choice.templateData())

   return render_template(choice.html, **templateData)

@app.route("/do/<item>/<action>")
def do(item, action):
   print "Item"
   print item
   print "Action"
   print action

   # Searching the item
   r = [x for x in domoWebModule.domoWebModules if x.name == item]
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
def listParameters():
   moduleList = []
   
   for x in domoWebModule.domoWebModules :
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

@app.route("/")
def accueil():
   templateData = {
      'tabList' :  domoWebModule.domoWebModules
   }
   return render_template('help.html', **templateData)

def strToClass(s):
   if s in globals() and isinstance(globals()[s], types.ClassType):
      return globals()[s]
   return None

#=============================================================
# Build the webui from config file
#=============================================================
def buildWebui(config):
   logger = logging.getLogger('domoweb')
   tabList = config.items('tabs')
   for modName, modType in tabList :
      logger.info("Loading tab " + modName + " (type " + modType +")")

      # Retrieve the module class
      domoWebModuleClass = strToClass(modType)
      
      # Create the object 
      domoModule = domoWebModuleClass(modName)

      # Set options from the config
      domoModule.setOptions(config.items(modName))

#-------------------------------------------------------------
# Run the web server
#-------------------------------------------------------------
   logger.info("Lancement du serveur web")
   app.run(host='0.0.0.0', port=8081, debug=False)
  

