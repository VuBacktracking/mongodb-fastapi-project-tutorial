import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import dotenv_values
from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from routes.api import router as api_router

config = dotenv_values(".env")

def get_db_client():
    client = MongoClient(config["ATLAS_URI"])
    return client

def get_database(client: MongoClient):
    return client[config["DB_NAME"]]

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = get_db_client()
    app.database = get_database(app.mongodb_client)
    print("Project connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/", response_description="Root route")
async def read_root():
    return {"message": "Welcome to the API"}

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000, log_level="info", reload=True)