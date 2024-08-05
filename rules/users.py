import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.users import User

def get_users_collection(request: Request):
    return request.app.database["users"]

def create_user(request: Request, user: User):
    user = jsonable_encoder(user)
    new_user = get_users_collection(request).insert_one(user)
    created_user = get_users_collection(request).find_one({"_id": new_user.inserted_id})
    return created_user

def list_users(request: Request, limit: int):
    users = list(get_users_collection(request).find(limit=limit))
    return users

def find_user(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    
    user = get_users_collection(request).find_one({"_id": ObjectId(id)})
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

def delete_user(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    deleted_user = get_users_collection(request).delete_one({"_id": ObjectId(id)})
    if deleted_user.deleted_count == 1:
        return {"message": f"User with id {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
