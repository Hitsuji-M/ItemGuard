from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from datetime import datetime as dt

from database.tables import *
from models import *


def logs_query(db: Session, limit: int = 0, desc: bool = True, before: dt = None) -> List[Log]:
    """
    Returns a list of logs based on 3 parameters :
    - Number limit of logs
    - Ascendant or Descendent order (based on the date)
    - Date limit (skip all logs with a more recent date than the one given)
    """

    query = db.query(Log)
    if desc:
        query = query.order_by(Log.logdate.desc())
    else:
        query = query.order_by(Log.logdate)

    if before and before < dt.now():
        query = query.filter(Log.logdate <= before)

    if limit and limit > 0:
        query = query.limit(limit)
    return query.all()

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
    """Add a log in the database (called automatically by creat/update/delete products services)"""
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

