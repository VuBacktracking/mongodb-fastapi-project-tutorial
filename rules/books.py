import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.books import Books, UpdateBooks
from bson import ObjectId

def get_books_collection(request: Request):
    return request.app.database["books"]

def create_book(request:Request, book: Books):
    book = jsonable_encoder(book)
    new_book = get_books_collection(request).insert_one(book)
    created_book = get_books_collection(request).find_one({"_id" : new_book.inserted_id})
    return create_book

def update_book(request: Request, id: str, book: UpdateBooks):
    book = {k : v for k,v in dict(book).items if v is not None}
    if len(book) > 1:
        update_result = get_books_collection(request).update_one({"_id": ObjectId}, {"$set": book})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")
    
    if (existing_book := get_books_collection(request).find_one({"_id": ObjectId(id)})) is not None:
        return existing_book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")

def list_books(request: Request, limit= int):
    books = list(get_books_collection(request).find(limit=limit))
    return books

def list_books_by_id(request: Request, id: str):
    if (book := get_books_collection(request).find_one({"_id": ObjectId(id)})):
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")

def list_books_by_author(request: Request, author: str):
    books = list(get_books_collection(request).aggregate([{"$match": {"author": author}}]))
    return books

def delete_book(request: Request, id: str):
    deleted_book = get_books_collection(request).delete_one({"_id": ObjectId(id)})

    if deleted_book.deleted_count == 1:
        return f"Book with ID {id} deleted sucessfully!"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found!")