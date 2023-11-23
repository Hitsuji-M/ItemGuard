CREATE TABLE IF NOT EXISTS itemg.LogType (
    idType SERIAL,
    nameLog VARCHAR(32),
    PRIMARY KEY(idType)
);

CREATE TABLE IF NOT EXISTS itemg.Log (
    idLog SERIAL,
    idType INT NOT NULL,
    logDate TIMESTAMP,
    PRIMARY KEY(idLog),
    CONSTRAINT fk_type_log_id FOREIGN KEY(idType) REFERENCES itemg.LogType(idType)
);

CREATE TABLE IF NOT EXISTS itemg.ProductType (
    idType SERIAL,
    nameType VARCHAR(32),
    PRIMARY KEY(idType)
);

CREATE TABLE IF NOT EXISTS itemg.Product (
    idProduct SERIAL,
    idType INT NOT NULL,
    price REAL DEFAULT 0.0,
    PRIMARY KEY(idProduct),
    CONSTRAINT fk_type_product_id FOREIGN KEY(idType) REFERENCES itemg.ProductType(idType)
);

CREATE TABLE IF NOT EXISTS itemg.User (
    idUser SERIAL,
    username VARCHAR(63) NOT NULL,
    passwd VARCHAR(65) NOT NULL,
    administrator BOOLEAN DEFAULT 0
)