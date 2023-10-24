from fastapi import FastAPI

from database.setup_db import engine, SessionLocal, BaseSQL

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

@app.get("/log/last")
def last_log():
    return BaseSQL.classes.items()