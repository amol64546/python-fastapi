import os

from fastapi import FastAPI
from app.routers import user_routers
from app.utils import vault_client
from app.utils.mongodb_client import MongoDBClient

app = FastAPI(
    title="FastAPI Sample Project",
    description="A sample FastAPI project for demonstration purposes",
    version="1.0.0",
)
mongodb_client = MongoDBClient()


# Include routers
app.include_router(user_routers.router, prefix="/users")
app.include_router(vault_client.router, prefix="/vault")



@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Sample Project"}

@app.get("/switch_db/{name}")
def switch_database(name: str):
    mongodb_client.switch_database(name)
    return mongodb_client.get_current_database().name