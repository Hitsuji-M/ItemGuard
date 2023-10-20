# ItemGuard


## Gestion des stocks :

Base de données comprenant plusieurs produits différents. Gestion quantité / entrée ou sortie de produit (logs) / gestion de la zone de rangement (ex: 20 objets par ligne, donc gestion du déplacement de produit) 


## Fonctionnalités:

Rajouter / enlever / consulter un ou plusieurs objets / voir les logs (Filtre date peut être) / 


## Architecture :

### BDD
- Table LogType
- Table Log
- (Table Utilisateur)
- Table Produit
- Table TypeProduit
- Table Zone ?


## Technos

- Python
- FastAPI
- PostgreSQL
- Redis ?


## Idées ++

Différents utilisateurs, admin (modifier les stocks) / regular (Juste regarder) 
Certains produits sont cachés (seulement accessible pour certains utilisateurs) peut être

--> Redis nécessaire pour donner de session (ou gestion des cookies)