from fastapi import APIRouter

from app.models.user import User
from app.utils.mongodb_client import MongoDBClient
from fastapi import HTTPException

router = APIRouter()

mongodb_client = MongoDBClient()

@router.post("")
def create_user(user: User):
    """
    Create a new user and insert into MongoDB.
    """
    try:
        return mongodb_client.insert_one("users", user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("")
def get_users():
    """
    Get all users from MongoDB.
    """
    try:
        users_from_db = mongodb_client.get_all_documents("users")
        for user in users_from_db:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
        return {"users": users_from_db}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")




