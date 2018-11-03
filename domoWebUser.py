#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# User definition
#========================================================
import logging
import string

from flask_login import \
   LoginManager, UserMixin, \
   login_required, login_user, logout_user, current_user

#adminUser = None
#allUser = None

class User(UserMixin):
    # proxy for a database of users
    user_database = {}

    def __init__(self, username, password):
        self.logger = logging.getLogger('domoweb')
        user = User.get(username)
        if (user is None) :
           self.id = username
           self.password = password
           User.user_database.update({username: self})
           self.logger.info("User '"+username+"' created")
        else :
           self = user
           self.password = password
           self.logger.info("User '"+username+"' updated")

    @property
    def is_authenticated(self):
        return True

    def name(self):
        return self.id

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

#-------------------------------------------------------------
# Initialization of the user management
#-------------------------------------------------------------
def domoWebUserInit(config, logger, debugFlags) :
   #global adminUser
   #global allUser

   # These ones are hard coded
   #adminUser = User("admin", "admin")
   #allUser = User("all", "admin")

   User("admin", "admin")
   User("all", "admin")

   # Then we create/modify based on the config
   if (('users' in debugFlags)  or ('all' in debugFlags)) :
      logger.debug("-- User creation ...")

   if (config.has_section('users')) :
      tabList = config.items('users')
      for login, desc in tabList :
         lines = string.split(desc, ":")
         User(login, lines[0])
    
