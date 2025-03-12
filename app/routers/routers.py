import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.models.user import User, CreateUser
from app.utils.mongodb_client import MongoDBClient

router = APIRouter()
logger = logging.getLogger(__name__)


mongodb_client = MongoDBClient()


@router.post("/users", response_model=User)
def create_user(user: CreateUser) -> User:
    """
    Create a new user and insert into MongoDB.
    """
    try:
        inserted_user = mongodb_client.insert_one("users", user)
        # Return the created user, converted to a User Pydantic model
        user_dict = user.dict()  # Convert Pydantic model to dictionary
        user_dict["id"] = str(inserted_user["_id"])  # Convert ObjectId to string

        # Return the user with the added "id"
        return User(**user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.get("/users", response_model=List[User])
def get_users() -> List[User]:
    # Example of a function comment inside 1
    """
    Get all users from MongoDB.
    """
    # Example of a function comment inside 2
    try:
        users_from_db = mongodb_client.get_all_documents("users")
        for user in users_from_db:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
        return {"users": users_from_db}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    """
    Get all users from MongoDB 2.
    """

@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: str) -> User:
    """
    Get a user by their unique user ID from MongoDB.
    """
    try:
        user_from_db = mongodb_client.get_document_by_id("users", user_id)
        if user_from_db:
            user_from_db["_id"] = str(user_from_db["_id"])  # Convert ObjectId to string for JSON serialization
            return {"user": user_from_db}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


def a():
    b()
    c()

def b():
    c()
    d()

def c():
    d()

def d():
    pass
