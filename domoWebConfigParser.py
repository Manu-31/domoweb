# -*- coding: utf-8 -*-
#=============================================================
# A configuraion tool for domoWeb based on python ConfigParser
#=============================================================
import ConfigParser

config = ConfigParser.ConfigParser()
config.optionxform = str

#-------------------------------------------------------------
# Lecture du fichier de configuration
#
# On va chercher la configuration dans les fichiers suivants et dans
# cet ordre
#   le fichier fourni en paramètre
#   ${HOME}/.domoweb.cfg
#   (A FAIRE)
#   /etc/domoweb.cfg
#config.read(['/etc/domoweb.cfg', os.path.expanduser('~/.domoweb.cfg')])
#config.read([os.path.expanduser('~/.domoweb.cfg')])
#-------------------------------------------------------------
def configParserInit(configFileName) :
    if (configFileName is None) :
        configFileName = os.path.expanduser('~/.domoweb.cfg')
        
    print "Reading configuration from '"+configFileName+"'"

    config.read(configFileName)

    
