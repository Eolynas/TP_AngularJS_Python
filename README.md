# TP Python/AngularJS

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)]()
[![made-with-python](https://img.shields.io/badge/Made%20with-AngularJS-1f425f.svg)]()
[![version-python](https://img.shields.io/static/v1?label=Python&message=3.7&color=065535)]()
[![version-python](https://img.shields.io/static/v1?label=AngularJS&message=1.7.9&color=065535)]()


# Détail du projet
- Créer une interface permmttant de gérer des interventions
- Cette interface contient:
  - un tableau listant les interventions
  - un bouton d'ajout d'intervention
- Le bouton d'ajout d'intervention ouvre un modale contenant un formulaire
- Il doit être possible de modifier & supprimer une intervention
- L'affichage des interventions peut être ordonnée de la plus récente à la plus ancienne
- Une intervention possède un statut parmi les suivants:
  - "Brouillon"
  - "Validé"
  - "Terminé"


## Installation

- Cloner le dépot
```
git clone https://github.com/Eolynas/TP_AngularJS_Python.git
```

Création d'un environnement virtuel (/!\ Attention à la version)
```
pip install virtualenv
virtualenv -p /usr/bin/python3.7 venv

source venv/bin/activate
```

- Installation des dépendances:
```
pip install -r requirements.txt
```

- Lancement du programme:
```
flask run
```

###Variable d'environnement
```
SECRET_KEY: secret key de votre application flask
```

-----------------
## Futur amélioration

- Ajout / amélioration de test unitaire pour la partie flask (python)
- Création de test unitaire pour la partie AngularJS
- Ajout d'une pagination pour le tableau
- Ajout d'un champs de recherche pour les interventions
- Création d'un vrai design
- Gestion des doublons


 -----------------
## Auteur
Développeur: Eddy Hubert

Contact: contact@eddy-hubert.fr
