CREATE TABLE IF NOT EXISTS itemg.LogType (
    idType SERIAL,
    nameLog VARCHAR(32),
    PRIMARY KEY(idType)
);

CREATE TABLE IF NOT EXISTS itemg.Log (
    idLog SERIAL,
    idType INT,
    logDate TIMESTAMP,
    PRIMARY KEY(idLog),
    CONSTRAINT fk_type_log_id FOREIGN KEY(idType) REFERENCES itemg.LogType(idType)
);