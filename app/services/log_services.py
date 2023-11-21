from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from database.tables import *
from models import *

def get_logs(db: Session) -> List[Log]:
    return db.query(Log).order_by(Log.logdate.desc()).all()

def get_log_by_id(db: Session, id: int) -> Log:
    record = db.query(Log).filter(id == Log.idlog).first()
    if not record:
        raise HTTPException(status_code=404, detail="Log not found")
    return record

def get_logs_limited(db: Session, limit: int) -> List[Log]:
    if limit <= 0:
        raise HTTPException(status_code=412, detail="Must show at least 1 log")
    return db.query(Log).order_by(Log.logdate.desc()).limit(limit).all()

def add_log(db: Session, model: LogModel) -> int:
    if not model.idType:
        raise HTTPException(status_code=422, detail="Missing values")
    new_log = Log(idtype=model.idType, logdate=model.logDate)
    db.add(new_log)
    db.commit()
    return new_log.idlog

def delete_log_by_id(db: Session, id: int) -> int:
    log = get_log_by_id(db, id)
    db.delete(log)
    db.commit()
    return log.idlog

