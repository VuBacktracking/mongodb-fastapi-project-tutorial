import uuid
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Books(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    description: str
    price: float = Field(gt=0)
    author: str
    pages: int = Field(gt=0)
    genre: str

    @field_validator('genre')
    def genre_validation(cls, genre):
        allowed_genres = ["Fiction", "Non-fiction"]
        if genre not in allowed_genres:
            raise ValueError(f'Genre must be one of {allowed_genres}')
        return genre

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Flowers for Algernon",
                "description": "",
                "price": 25,
                "author": "",
                "pages": 417,
                "genre": "Fiction"
            }
        }

class UpdateBooks(BaseModel):
    title: Optional[str] 
    description: Optional[str]
    price: Optional[float]
    author: Optional[str]
    pages: Optional[int]
    genre: Optional[str]
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Flowers for Algernon",
                "description": "Such a great book!",
                "price": 20,
                "author": "Daniel Keyes",
                "pages": 300,
                "genre": "Fiction"
            }
        }
