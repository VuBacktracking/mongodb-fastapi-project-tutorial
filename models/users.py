import uuid
from pydantic import BaseModel, Field, SecretStr, EmailStr

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    email: EmailStr = Field(...)
    password: SecretStr

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "VuPhan",
                "email": "VuPhan@gmail.com",
                "password": "vuphan.here"
            }
        }
