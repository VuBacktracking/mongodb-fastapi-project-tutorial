import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.addresses import UserAddress, UpdateAddress

def get_addresses_collection(request: Request):
    return request.app.database["addresses"]

def create_addrs(request: Request, user_addrs: UserAddress):
    user_addrs = jsonable_encoder(user_addrs)
    new_addrs = get_addresses_collection(request).insert_one(user_addrs)
    created_addrs = get_addresses_collection(request).find_one({"_id": new_addrs.inserted_id})
    return created_addrs

def list_addrs(request: Request, limit: int):
    addrs = list(get_addresses_collection(request).find(limit=limit))
    return addrs

def find_addrs(request: Request, user_id: str):
    addrs = list(get_addresses_collection(request).find({"user_id": user_id}))
    if addrs:
        return addrs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Addresses for user_id {user_id} not found")

def update_addrs(request: Request, id: str, addrs: UpdateAddress):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    update_result = get_addresses_collection(request).update_one(
        {"_id": ObjectId(id)},
        {"$set": addrs.dict(exclude_unset=True)}
    )

    if update_result.modified_count == 1:
        updated_addrs = get_addresses_collection(request).find_one({"_id": ObjectId(id)})
        return updated_addrs

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id {id} not found")

def delete_addrs(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    delete_result = get_addresses_collection(request).delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Address with id {id} deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id {id} not found")
