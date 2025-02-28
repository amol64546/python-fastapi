import logging

import pandas as pd
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from neo4j import Result

from app.models.request_models import Ontology
from app.models.user import User
from app.utils.mongodb_client import MongoDBClient
from app.utils.neo4j_client import Neo4jClient
from app.utils.query_utils import Queries

router = APIRouter()

mongodb_client = MongoDBClient()
logger = logging.getLogger(__name__)
neo4j_client = Neo4jClient()

@router.post("/users")
def create_user_1(user: User):
    """
    Create a new user and insert into MongoDB.
    """
    try:
        return mongodb_client.insert_one("users", user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

def test() -> str:
    return "Hello World"

# Example of a function comment outside 0
"""
Get all users from MongoDB 0
"""
@router.get("/users")
def get_users():
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

@router.get("/users/{user_id}")
def get_user_by_id(user_id: str):
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


def db_query(username, ontology_id, cypher: str, params=None) -> pd.DataFrame:
    """Executes a Cypher statement and returns a DataFrame"""
    if params is None:
        params = {}
    try:
        db_name = f"d{username}-{ontology_id}"
        neo4j_client.switch_database(db_name)
        return neo4j_client.execute_query(
            cypher, parameters=params, result_transformer=Result.to_df
        )
    except Exception as e:
        """Executes a Cypher statement and returns a DataFrame 2"""
        # Log the exact error
        logger.error(f"Cypher query failed. Query: {cypher}, Params: {params}, Error: {str(e)}")
        return pd.DataFrame()

@router.post('/users/create')
def create_user(name, email):
    """Create a new user with name and email."""
    data = request.json  # request body
    return {"message": "User created", "user": data}  # response body

def import_ontology_neo4j(username, ontology_id, ontology_url, file_type, ontology_type):
    try:

        # Parameters to be passed into the query
        params = {
            "ontology_url": ontology_url,
            "file_type": file_type,
            "ontology_type": ontology_type
        }

        # Execute the query with parameters and capture the result
        return db_query(username, ontology_id, Queries.ONTOLOGY_FINAL_QUERY, params)

    except Exception as e:
        # Log the error and raise the exception again to propagate it
        logger.error(f"Failed while importing the ontology: {str(e)}")
        raise


@router.post("/import-ontology")
def import_ontology(ontology: Ontology):
    try:
        doc_metadata_req = {
            "ontologyName": ontology.ontology_name
        }

        mongo_collection = mongodb_client.get_mongo_collection("ontology_creation")
        result = mongo_collection.insert_one(doc_metadata_req)

        doc_metadata_req["_id"] = str(result.inserted_id)

        # Call the function to import the ontology and capture the result
        result = import_ontology_neo4j(ontology.tenant_id, str(result.inserted_id), ontology.ontologyUrl,
                                       ontology.file_type,
                                       ontology.ontology_name)

        return JSONResponse(doc_metadata_req, status_code=200)

    except Exception as e:
        logger.error(f"Error while importing ontology: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to import ontology: {str(e)}")
