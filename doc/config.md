# Structure de la configuration
-------------------------------

   L'idée est de construire des objets éventuellement complexes en
associant des briques simples.

   C'est une liste de sections, par exemple

'''
[general]
logConsole = True

[tabs]
aide = help
debogage = debug
login = signin
'''

   Certains noms de section sont réservés à un usage bien spécifique,
par exemple general, users, modules et tabs.

   Chaque module doit être décrit par une section qui lui est propre
ou comme attribut d'un autre module définit lui-même dans sa section.
Une section spécifique permet de lister (voire de définir) les modules
qui sont affichés dans l'interface graphique (la section [tab]) et une
autre permet de lister des modules qui ne sont pas visibles bien que
actifs (la section [modules]).

# Format général d'une section
------------------------------

   Une section de base définit donc un module. Elle a la structure
suivante :

'''
[example]
type = generic
message = C'est un petit pas pour l'homme, un grand pas pour \
l'humanité
html = generic.html
'''

   Ici un module de nom 'exemple' et doté des attributs type, message
et html est défini.

# La section [modules]
----------------------

   Elle permet de lister les modules qui ne constituent pas des
onglets affichés. C'est une liste de lignes définissant chacune un
module. Chaque ligne est d'une des formes suivantes

'''
nom = t\_name[,param]
nom = s\_name
nom = chaine
'''

  * Si le type 't\_name' est connu, alors le module 'nom' est créé avec
  les paramètres fournis (tout paramètre non fourni prend sa valeur
  par défaut).
    Si, de plus, une section 't\_name' existe, alors elle est lue pour
  mettre à jour les champs du module 'nom'.

  * Si le type 's\_name' n'existe pas, et si la section 's\_name'
  existe, alors le module 'nom' est créé avec la définition de la
  section 's_name'

# La section [tabs]
-------------------

Elle donne la liste des onglets affichés par l'interface web. Ils y
sont définis comme dans la section [modules].

# La section [general]
----------------------

Elle spécifie la configuration génrale du système. Les éléments
suivants peuvent être configurés 

## port

   Il définit le port d'écoute du serveur web. Par exemple

port = 8082

   Il est facultatif, la valeur par défaut est 8081.

## logFileName

## logConsole

## debugFlags

# La section [users]
--------------------

Elle permet de définir des utilisateurs, un par ligne, de la façon
suivante 

nom = password:description

   Pour le moment, le mot de passe est en clair ! Et oui, ...

   Un exemple

'''
[users]
admin = nimda:Administrateur du système
manu = manu:Manu Chaput
chaput = chaput:Famille Chaput
visiteur = visiteur:Utilisateur curieux
''''

# La gestion des droits
-----------------------

   Chaque module comporte deux attributs dédiés à la gestion des
droits : readAccess et writeAccess. Ils donnent respectivement la
liste des utilisateurs ayant le droit de consulter et modifier le
module.

   Cahque attribut est défini de l'une des façons suivantes;
   
   * Une liste de noms d'utilisateurs séparés par des virgules
     (readAccess=admin,manu).
   * La valeur 'all' stipule que n'importe quel utilisateur identifié
     est autorisé.
   * La valeur '*' signifie que la permission est accordée à tout le
     monde (y compris un utilisateur non défini). C'est la valeur par
     défaut pour un objet de type 'signin' car il doit être utilisable
     même non connecté afin de permettre ... de se connecter !


