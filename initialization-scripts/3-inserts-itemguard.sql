INSERT INTO
    itemg.ProductType
VALUES
    (1, 'Boisson'),
    (2, 'Biscuits');


INSERT INTO
    itemg.LogType(idType, nameLog)
VALUES
    (1, 'Ajout produit'),
    (2, 'Modification produit'),
    (3, 'Suppression produit');


INSERT INTO itemg.User VALUES(1, 'admin@itemg.fr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', true);