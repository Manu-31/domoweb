# Liste des moules et de leurs attributs

   Voici une liste des modules définis avec entre parenthèse la liste
des attributs qu'ils définissent. Chaque module hérite des attributs
de ses ancètres.
   
  . domoWebModule
     . debug
	 . help
	 . embed
	 . domoWebDevice
	   . domoWebSwitchDevice (status)
   	     . remoteSwitchDevice
		 . gpioSwitch (pin, direction)
       . domoWebThermometer
	     . oneWireThermometer
	     . remoteThermometer
	 . domoWebDataCache
	   . domoWebCircularDataCache

# Caractéristiques de chaque module

## domoWebSwitchDevice
   -------------------
   
### Ancètres

   . domoWebModule
	 . domoWebDevice
	   . domoWebSwitchDevice

### Les attributs

#### status

   Indique l'état (activé ou non) du switch.

   Modifiable : oui
   
   Valeurs : 0 ou 1, 'on' ou 'off'

## gpioSwitch
   ----------
 
### Ancètres

   . domoWebModule
	 . domoWebDevice
	   . domoWebSwitchDevice
         . gpioSwitch

### Les attributs

#### pin

   Indique le numéro de la broche à utiliser
   
   Modifiable : oui
   
   Valeurs : entier
