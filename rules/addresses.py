import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.addresses import UserAddress, UpdateAddress
from bson import ObjectId

def get_addrs_collection(request: Request):
    return request.app.database["addresses"]

def create_addrs(request: Request, user: UserAddress = Body(...)):
    addrs = jsonable_encoder(user)
    new_addrs = get_addrs_collection(request).insert_one(addrs)
    created_addrs = get_addrs_collection(request).find_one({"_id": new_addrs.inserted_id})
    return created_addrs


def list_addrs(request: Request, limit: int):
    addrs = list(get_addrs_collection(request).find(limit = limit))
    return addrs


def find_addrs(request: Request, user_id: str):
    user_addrs = list(get_addrs_collection(request).find({"user_id": user_id}))
    if len(user_addrs):
        return user_addrs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User has no address yet.")

def update_addrs(request: Request, id: str, addrs: UpdateAddress = Body(...)):
    addrs = {k: v for k, v in addrs.dict().items() if v is not None} #loop in the dict 
    if len(addrs) >= 1:
        update_result = get_addrs_collection(request).update_one({"_id": ObjectId(id)}, {"$set": addrs})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address not found!")

    if (existing_item := get_addrs_collection(request).find_one({"_id": ObjectId(id)})) is not None:
        return existing_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")

def delete_addrs(request: Request, id: str):
    deleted_addrs = get_addrs_collection(request).delete_one({"_id": ObjectId(id)})

    if deleted_addrs.deleted_count == 1:
        return f"Address deleted sucessfully!"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address not found!")