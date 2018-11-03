# Mon premier projet : un aquarium

   Je veux gérer l'éclairage, la filration et la température de mon
aquarium avec DomoWeb.

   Supposons que j'ai une sonde thermique 1wire et un relai de
commande piloté par le GPIO de mon raspberry permettant de contrôler
l'éclairage .

   Je veux permettre à tout le monde de voir l'état de mon aquarium et
à un utilisateur spécifique de contrôler l'éclairage.

## Le fichier de configuration

   Il ressemble à ceci (examples/basicmodules.cfg). Dans un premier
temps, décrivons les utilisateurs :

'''
[users]
manu = manu:Manu Chaput
visiteur = visiteur:Utilisateur curieux
'''
   
   Maintenant nous allons décrire le thermomètre :
   
'''
[thermo1]
type=oneWireThermometer
address = 28-031464227dff
readAccess=*
html=thermometerGeneric.html
'''

   On donne son type ('oneWireThermometer') puis son addresse (ici
'28-031464227dff').

   On souhaite qu'il soit accessible en lecture par tout le monde,
même sans être identifié.
   
   Enfin, on définit la page html à utiliser pour le visualiser.

   Passons maintenant à l'interrupteur permettant de piloter
l'éclairage. Il est défini comme suit :

'''
[bouton1]
type = gpioSwitch
pin = 36
readAccess = all
writeAccess = admin,manu
html = switchGeneric.html
'''

   Ici encore, on définit son type et les paramètres qui y sont liés
(la broche est ici identifiée par l'attribut 'pin').

   On souhaite qu'il soit consultable par n'importe quel utilisateur
identifié ('readAccess = all') et modifiable par admin et manu.

   Il nous suffit maintenant de lister dans la section 'tabs' les
modules à afficher :

'''
[tabs]
aide = help
debogage = debug
therm=thermo1
btn=bouton1
login = signin
'''

   Et le tour est joué !
   
# Deuxième étape : un meilleur affichage

   Si on n'est pas ravi par l'affichage, on peut créér soi-même des
pages permettant d'améliorer le rendu. En ce qui concerne notre
aquarium, nous avons créé un fichier 'templates/aquarium.html'. Mais
avant de le décrire, il nous faut modifier le fichier de configuration
afin d'intégrer les modules au sein d'un seul module plus riche.

   A SUIVRE ...
   
   Teaser : description de aquarium.cfg et aquarium.html 

# Troisième étape : des actions

   Le fichier de configuration est 'examples/actions.cfg'
   
   Imaginons que nous souhaitions activer et désactiver le chauffage
en fonction de la température. Comme faire cela ? Nous allons utiliser
un nouveau type d'objets : les actions. Définissons-en deux de la
façon suivante

'''
[allumerChauffage]
type = domoWebAction
object = bouton1
attribute = status
value = on

[couperChauffage]
type = domoWebAction
object = "bouton1"
attribute = status
value = off
'''

   Nous supposons donc ici que le 'bouton1' active le chauffage.
   
   Il nous reste maintenant à demander au thermomètre de déclancher
ces actions en fonction de seuils :

'''
[thermo1]
type=oneWireThermometer
address = 28-031464227dff
html=thermometerGeneric.html
minimum = 26
maximum = 32
actionLow = allumerChauffage
actionHigh = couperChauffage
readAccess=*
'''

   Ici, on a défini un seuil bas 'minimum' et un sueil haut 'maximum',
et on a affecté les actions préalablement définies. Le chauffage sera
allumé si la température descend sous la valeur donnée à 'minimum' et
éteind il cette température monte au delà de la valeur de 'maximum'.

# Quatrième étape : éditer les paramètres

   OK, c'est sympa tout ça, mais doit-on modifier le fichier de
configuration dès que l'on souhaite modifier un paramètre ?
Heureusement non ! 

   On peut construire une page web dans laquelle les principaux
paramètres pourront être édités.

   [exemple]

   Attention, les paramètres ainsi modifiés ne le sont que durant la
session en cours. Pour une prise en compte au prochain démarrage, il
est nécessaire de mettre à jour le fichier de configuration.
