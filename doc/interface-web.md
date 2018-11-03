   A voir : faire un sous répertoire pour les modules. Par exemple
thermometer.hml affiche une page avec un thermomêtre, mais
modules/thermometer.html doit être inclu là où on veut mettre un
thermometre. Du coup le premier inclu le second.

   A voir aussi : faire un défault avec jinja2 : si ${theme}/toto.html
   n'existe pas, on va chercher defaut/toto.html


# Structure générale de l'arborescence des fichiers

   J'utilise actuellement flask. Les fichiers sont répartis de la
façon suivante :
   
templates/
  ├── domoweb.html
  ├── head.html
  ├── bottom-line.html
  ├── thermometerGeneric.html
  ├── default
        ├── thermometer.html
        ├── temphist.html
        ├── switch.html
        ├── switch-light.html
  ├── echarts
        ├── thermometer.html
  ├── chartist
        ├── thermometer.html

  
static/
  ├── style.css

   Flask se fonde sur jinja2 qui introduit la notion d'héritage
entre les fichiers. Nous avons ainsi par exemple :

   domoweb.html
     ├── thermometerGeneric.html

   Je ne me suis pas encore complètement fait une religion, mais
l'idée serait de pouvoir utiliser 'toto.html' sans se préoccuper du
thème. Donc dans 'toto.html' il y aurait un 'include theme/toto.html'
avec l'héritage qui permet de retomber sur le thème par défaut. Mais
il faut aussi définir une règle de nommage : thermometer.html ne peut
pas ête à la fois une 'page' qui décrit un thermomètre et un objet
dans une page plus complexe. Ou alors peut-être que si ! Pour le
moment non : une page de plus haut niveau hérite de domoweb.html et
doit définir mainblock, ...
   
# Gestion des thèmes

   L'interface de chaque objet (thermomètre, switch, ...) est décrite
dans un fichier qui doit être présent dans chacun des répertoires de
thème. Ce fichier doit effectivement décrire l'interface en héritant
de son équivalent dans le thème 'default' puis en surchargeant le bloc
principal.

   À titre d'exemple, le fichier default/thermometer.html contient les
lignes suivantes :

'''
{% block thermometer %}
<div class="w3-container w3-blue w3-center">
   <div class="w3-medium"> {{ name | default("Température") }}</div>
   <div class="w3-jumbo"> {{ thermometer.getAttribute('temperature') }}°</div>
</div>
{% endblock %}
'''

   Le fichier echarts/thermometer.html contient quant à lui des choses
du genre :

'''
{% extends "default/thermometer.html" %}

{% block thermometer %}

<div class="w3-container w3-white w3-center">
<div id="chart" style="width: 40vw; height: 40vh;">
</div>
</div>

<script>
 ...
</script>

{% endblock %}
'''

   Enfin, le fichier toto/thermometer.html d'un thème qui ne définit
pas de nouvelle version du thermomètre contient simplement :

'''
{% extends "default/thermometer.html" %}
'''
   
# Structure des fichiers 

   Le ficher de base est domoweb.html, il définit une structure avec
un entête, un corps principal puis un bas de page. Pour cela les
fichiers suivants sont inclus :

   * 'head.html' pour définir tout ce qui est nécessaire (chargement de
    librairies, ...)
   * 'menu.html' pour construire le menu permettant de naviguer entre
    les modules disponibles
   * 'bottom-line.html' pour des informations en bas de page
	
	Le corps principal est défini par un bloc 'maincontent' que
doivent instancier les fichiers qui héritent de domoweb.html'
