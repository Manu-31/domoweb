#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================
# Management of domoWebModules
#
# This file basically builds up modules based on a config structure
# built from a config file
#=============================================================

# Import available modules
from domoWebModule import *
from domoWebModule import domoWebModule as generic
from domoWebSignIn import *
from oneWireDevice import *
from gpioDevice import *
from domoWebAction import domoWebAction


def strToClass(s):
   if s in globals() and issubclass(globals()[s], domoWebModule):
      return globals()[s]
   return None

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
#   Je tente d'introduire un
#
#   (1bis) value = type
#   avec une section [value] définie ailleurs
#   pour le moment le soucis est sur la définition du type
#
#   NON ! CECI n'a pas de sens !!! Le (1bis) c'est simplement le cas
# où le module n'est pas encore défini car sa section n'a pas été
# lue. Ce qui est le cas par défaut a priori pour le moment puisqu'on
# ne lit par défaut que [modules] et [tabs]
#

#   ATTENTION, le soucis vient de l'ambiguité entre (1), (1bis) et
# (2). Dans minimal.cfg par exemple il y a une section debug (normal)
# et un tab "debogage = debug" car debug est aussi un type. Bref, il
# faut que je me fixe une syntaxe, un ordre de priorité en cas de
# doublons de ce genre, ... avant de débuger une situation qui est
# foireuse car mal définie !!
#
#   On pourra éventuellement définir un value = type:section
#
def stringToDomoWebModule(name, value, config) :
   attrParam = string.split(value, ",")
   attrType = attrParam.pop(0)

   # if the first list element is the name of a predefined module
   # (1) case "value = previously_defined_name"
   predefAttr = getDomoWebModuleByName(attrType)
   if (predefAttr is not None) :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("stringToDomoWebModule : '"+attrType+"' already defined")
      return predefAttr     

   # (1) bis : described in a section that has not been loaded
   # (default case for now)
   if (config.has_section(attrType)) :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("stringToDomoWebModule : found a '"+attrType+"' section")
      return createModuleFromSection(config, attrType)
         
   # (3) case "value = arbitrary string"
   attrCls = strToClass(attrType)
   if (attrCls is None) :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("stringToDomoWebModule '"+value+"' is a string" );
      result = value # eg strings

   # Is this a new module declaration ?
   # (2) case "value = attrType,attrParam"
   else :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("Création d'un '"+attrType+"' avec comme param :");
         logger.debug(attrParam)
      result = attrCls(name)
      print " ATTENTION : Paramètres à positionner ! *****"
   return result

# Create objects from an option list and add these attributes to a
# domoWebModule 
def addAttributes(dwm, optionList, config):
   ol = list(optionList)
   for name, value in ol :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("addAttributes : "+dwm.name+" reçoit un attribut '"+ name+"' de valeur '"+value+"'")

      # Reserved values  WARNING : pas top !
      if (name == "type") :
         if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
            logger.debug("On oublie ...")
      else :   
         # Create a module
         attr=stringToDomoWebModule(dwm.name+"."+name, value, config)

         # Add this as an attribute
         dwm.addAttribute(name, attr)
      
      del optionList[optionList.index((name, value))]

#-------------------------------------------------------------
#   Cette fonction était une tentative, mais je la sens mal !
#
# Creation of a single module from a section :
#
# [sectionName]
# type = <a_type>
# ...
#-------------------------------------------------------------
def createModuleFromSection(config, sectionName) :
   tabList = config.items(sectionName)

   if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
      logger.debug("createModuleFromSection(sectionName=" + sectionName + ") IN")

   result = None
   for n, v in tabList :
      if (n == "type") :
         if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
            logger.debug("It is a '"+v+"'")
         attrCls=strToClass(v)
         result = attrCls(sectionName)

   if (result is not None) :
      logger.debug("createModuleFromSection setting options, ...")

      # Set options from the config
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("Loading parameters for' " + sectionName + "'")

      addAttributes(result, config.items(sectionName), config)

      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("createModuleFromSection(sectionName=" + sectionName + ") OUT")
   else :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("No type for' " + sectionName + "', not created")
         
   return result

#-------------------------------------------------------------
# Creation of multiple modules described in a section of the config
# file. Such a section is a list of
#
# name = type
#
# where type is a subclass of domoWebModule
#
# Then a section [name] is searched for and read to configure the
# module
#-------------------------------------------------------------
def createModulesFromSection(config, sectionName, hidden) :
   # Let's build a genericDomoWebModule to host these modules
   section = domoWebModule(sectionName)
   
   tabList = config.items(sectionName)
   for modName, optionList in tabList :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("createModulesFromSection : " + modName + " (type/sec. " + optionList +")")
      domoModule = stringToDomoWebModule(modName, optionList, config)
      
      if hidden :
         domoModule.addAttribute('hidden', True)
      else :
         domoModule.addAttribute('hidden', False)

      section.addAttribute(modName, domoModule)
                    
#=============================================================
# module management initialization
#=============================================================
def domoWebModuleManagementInit(config, l, df) :
   global debugFlags
   global logger

   debugFlags = df
   logger = l
   
   if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
      logger.debug("*** domoWebModule initialization, ...")
   
   # Create hidden modules
   if (config.has_section('modules')) :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("-- Hidden modules creation ...")
         logger.debug("------------------------------")
      createModulesFromSection(config, 'modules', True)
   
   # Create tabs
   if (config.has_section('tabs')) :
      if (('objectCreation' in debugFlags) or ('all' in debugFlags)) :
         logger.debug("-- Public modules creation ...")   
         logger.debug("------------------------------")   
      createModulesFromSection(config, 'tabs', False)   
