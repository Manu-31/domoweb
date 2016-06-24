#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================================
# User definition
#========================================================
import logging

from flask_login import \
   LoginManager, UserMixin, \
   login_required, login_user, logout_user, current_user

class User(UserMixin):
    # proxy for a database of users
    user_database = {}

    def __init__(self, username, password):
        self.logger = logging.getLogger('domoweb')
        user = User.get(username)
        if (user is None) :
           print "Création de " + username
           self.id = username
           self.password = password
           User.user_database.update({username: self})
           self.logger.info("User '"+username+"' created")
        else :
           print "Modification de " + username
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

