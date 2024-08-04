import uuid
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Books(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias= "_id")
    title: str
    description: str
    price: float = Field(gt = 0)
    author: str
    pages: int = Field(gt = 0)
    genres: str

    @field_validator('genre')
    def genre_validation(cls, genre):
        genres = ["Fiction", "Non-fiction"]
        if genre not in genres:
             raise ValueError(f'Genre must be in {genres}')
        return genre
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Flowers for Algernon",
                "description": "",
                "price": 25,
                "author": "",
                "pages": 417,
                "genre": "Fiction"
            }
        }

class updateBooks(BaseModel):
    title: Optional[str] 
    description: Optional[str]
    price: Optional[float]
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Flowers for Algernon",
                "description": "Such a great book!",
                "price": 20
            }
        }