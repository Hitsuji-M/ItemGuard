from fastapi import FastAPI

app = FastAPI(
    title="ItemGuard",
    description="Inventory software",
    version="0.0.1",
)

@app.get("/")
def root():
    return "ItemGuard on"