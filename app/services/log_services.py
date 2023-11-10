from sqlalchemy.orm import Session

from database.tables import *

def all_logs(db: Session) -> list:
    return db.query(Log).all()