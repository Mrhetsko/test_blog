from fastapi import FastAPI
import models, router
from database import engine

# Create all the tables defined in models.py in database.
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Simple Blog API")

app.include_router(router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to demo Simple Blog API!"}