from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class User(CreateUser):
    id: str