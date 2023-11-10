from fastapi import FastAPI, Depends
from database.setup_db import engine, SessionLocal, BaseSQL
from database.models import Log
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI(
    title="ItemGuard",
    description="Inventory software",
    version="0.0.1",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return "ItemGuard on"


@app.get("/db/tables")
def last_log():
    return BaseSQL.classes.keys()

@app.get("/log/view")
def all_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs
