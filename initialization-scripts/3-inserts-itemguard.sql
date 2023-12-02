INSERT INTO
    itemg.ProductType(nameType)
VALUES
    ('Boisson'),
    ('Biscuits');


INSERT INTO
    itemg.LogType(nameLog)
VALUES
    ('Ajout produit'),
    ('Modification produit'),
    ('Suppression produit');


INSERT INTO itemg.User(email, passwd, fullName, administrator) VALUES('admin@itemg.fr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', true);
INSERT INTO itemg.User(email, passwd, fullName, administrator) VALUES('user@itemg.fr', '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb', 'user', false);