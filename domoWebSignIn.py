#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================

import domoWebModule
from domoWebUser import *

#=============================================================
# A login module 
#=============================================================
class signin(domoWebModule.domoWebModule) :
   def __init__(self, name, l=[], html="login.html") :
      domoWebModule.domoWebModule.__init__(self, name, html)
      self.setReadUsers(None)

#-------------------------------------------------------------
# The debugger page helper
#-------------------------------------------------------------
   def templateData(self):
      templateData = {}

      return templateData

   # The update method is used here to log in a user
   def update(self, dataDict):
      user = User.get(dataDict['username'])

      if (user is None) :
         print "Iconnu ..."
      else:
         if (user.password == dataDict['password']) :
            login_user(user)
