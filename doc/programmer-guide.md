# Les principales classes

domoWebModule
   domoWebDevice
      domoWebSwitchDevice            Pour les interrupteurs
         remoteSwitchDevice          A distance
	     gpioSwitch                  Sur le GPIO du RPi
      domoWebThermometer
         remoteThermometer
	     oneWireThermometer

# Gestion des attributs

   Chaque module a des attributs liés à domoWeb. Ces attributs sont
des attributs au sens de Python, mais sont également listés dans un
attribut (au sens Python) domoWebAttributes. Ils peuvent donc être
manipulés normalement dans le code. En revanche, toute manipulation
liée à l'interface web testera d'abord si les attributs à lire/écrire
sont des domoWebAttributes et si l'utilisateur a le droit, ... Cela
permet de plus de tenir à jour un 'logbook'.

   Il existe trois fonctions permettant de créer/modifier un attribut

   * setAttribute est loguée et ne peut que mettre à jour des
     attributs existants et identifiés, cette fonction est utilisée
     pour l'interface utilisateur, et c'est la seule qui doit être
     utilisée dans ce contexte (éventuellement via 'update()')
   * addAttribute permet de créer (s'il n'existe pas) un nouvel
	 attribut, pourvu qu'il ne corresponde pas à un attribut python. Il
	 est éventuellement initialisé avec setAttribute. Cette fonction est
	 utilisée lors de la lecture des fichiers de config. En effet, on
	 peut ajouter des attributs à un module. C'est même comme cela que
	 l'on compose des modules complexes.
   * turnAttribute permet de définir comme attribut un attribut
	 python pré-existant. Cette fonction est utiliée dans le
	 constructeur des modules.   

   Si on résume : dans webui.py on utilise uniquement setAttribute ou
update, dans domoWebModuleMgt on peut ajouter addAttribute, et dans
les classes héritièress de domoWebModule, tout est permis !

## Ajout d'un attribut

### La méthode addAttribute() de domoWebModule

   cette fonction ajoute un atttribut ou modifie sa valeur s'il
existe déjà. Un attribut dont le nom est déjà utilisé pour un attribut
non domoWeb n'est pas affecté.

### La méthode turnAttribute() de domoWebModule
   
### La méthode update() de domoWebModule

   Elle prend en paramètre un dictionnair et applique un
'setAttribute()' pour chaque élément.

# Gestion des utilisateurs

   Chaque module est caractérisé par une liste des utilisateurs qui
peuvent le consulter, nommée readAccess et une liste des utilisateurs
qui peuvent le modifier, nommée writeAccess.

   La classe user est définie dans le fichier domoWebUser.py mais ce
fichier ne définit que ça, pas leur utilisation, qui est définie dans
domoWebModule.py au travers d'attributs de la classe domoWebModule.

## Principe

   L'objectif est d'accorder ou de refuser la consultation ou la
   modification d'un module à un utilisateur. Certains modules peuvent
   être publics, c'est-à-dire accessibles même sans utilisateur
   identifié, c'est par exemple au moins le cas du module permettant
   de s'identifier, qui doit pouvoir être lu et modifié même sans
   utilisateur, par définition. D'autres peuvent être accessibles à
   tous les utilisateurs connus (la consultation d'une page d'aide par
   exemple). Les autres seront filtrés avec plus de précision.
   
## Implantation

   readUsers et writeUsers sont des listes d'utilisateurs. La
   signification est la suivante

   . None : pas de liste, pas de contrôle, tout le monde peut accéder 
   . [] : une liste vide signifie qu'aucun utilisateur ne peut accéder
   . [ a b c ] : les utilisateurs de la liste sont autorisés, les
   autres non
   . [ allUser ] : si l'utilisateur allUser est dans la liste, tout
   utilisateur connu peut accéder
   
## Initialisation de readAccess et writeAccess

   Ces deux champs sont des attributs (ajoutés comme tels via un appel
   à addAttribute) de type chaines de caractères. Elles sont
   initialisées à une chaîne vide ("") dans le créateur d'un
   domoWebModule.

## Modification de readAccess et writeAccess

   readAccess et writeAccess sont également définis comme des
   properties (au sens de Python) et donc dotés d'un setter.
   
### Utilisation du setter

   On peut

### Ajout d'un utilisateur

On peut ajouter un utilisateur en fonction de son nom avec

mod.addReadUser(User.get(nom))

## Vérification des droits

   Les droits sont vérifiés par les deux fonctions suivantes de la
   classe domoWebModule

userCanRead
userCanWrite

# L'affichage d'une interface Web

   L'interface Web est assurée par webui.py en se fondant sur le micro
framework flask.

   Nous ne décrirons ici que la structure de webui.py
   
   Les fichiers html, css, ... sont décrits dans un autre document
