# ItemGuard

## Instructions d'installation

Cloner le fichier dans un terminal:
- `git clone https://git.esiee.fr/massone/itemguard`
- `cd ItemGuard`
- `docker-compose up --build`

Aller sur localhost:8501 pour lancer streamlit

Se connecter avec les identifiants admin pour avoir l'accès complet:

admin@itemg.fr / admin

Ou

user@itemg.fr / user


## Présentation du projet

Notre objectif est de simuler une application de gestion des stocks. Notre application offre les possibilités suivantes:

- Créer, modifier, supprimer un produit (nom,prix,quantité)
- Une gestion des logs ainsi qu'un tri de ces logs en fonction de plusieurs paramètres
- Une gestion des utilisateurs avec des différences de permissions entre un utilisateur et un admin
- La modification de son profil

## Architecture

### BDD

- Table LogType
- Table Log
- Table Utilisateur
- Table Produit
- Table TypeProduit

## Packages utilisés

- Python
- FastAPI
- PostgreSQL
- Streamlit
- Adminer