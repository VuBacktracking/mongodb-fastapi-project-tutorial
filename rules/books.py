import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.books import Books, UpdateBooks

def get_books_collection(request: Request):
    return request.app.database["books"]

def create_book(request: Request, book: Books):
    book = jsonable_encoder(book)
    new_book = get_books_collection(request).insert_one(book)
    created_book = get_books_collection(request).find_one({"_id": new_book.inserted_id})
    return created_book

def update_book(request: Request, id: str, book: UpdateBooks):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    book_dict = book.dict(exclude_unset=True)
    updated_book = get_books_collection(request).find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": book_dict},
        return_document=True
    )
    if updated_book:
        return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

def list_books(request: Request, limit: int):
    books = list(get_books_collection(request).find(limit=limit))
    return books

def list_books_by_id(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    book = get_books_collection(request).find_one({"_id": ObjectId(id)})
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

def list_books_by_author(request: Request, author: str):
    books = list(get_books_collection(request).find({"author": author}))
    return books

def delete_book(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")

    deleted_book = get_books_collection(request).delete_one({"_id": ObjectId(id)})
    if deleted_book.deleted_count == 1:
        return {"message": f"Book with id {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
