import os

from pymongo import MongoClient
import logging



print(f"MONGO_URI: {os.getenv('MONGO_URI')}")

class MongoDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = MongoClient(os.getenv("MONGO_URI"))
            cls._instance.database = cls._instance.client["test"]
            logging.info("Connected to MongoDB")
        return cls._instance

    def switch_database(self, database_name):
        """
        Switch to a different database.
        
        :param database_name: Name of the database to switch to.
        """
        if not isinstance(database_name, str):
            raise ValueError("Database name must be a string")

        # Switch to the new database
        self._instance.database = self.client[database_name]
        print(f"Switched to database: {database_name}")

    def insert_one(self, collection_name, document):
        """
        Insert a single document into a specified collection.
        :param collection_name: The name of the collection.
        :param document: The document to insert (should be a dictionary or Pydantic model).
        :return: The inserted document with _id assigned by MongoDB.
        """
        collection = self.database[collection_name]
        document = document.dict()
        result = collection.insert_one(document)

        document["_id"] = str(result.inserted_id)
        return document

    def get_all_documents(self, collection_name):
        """
        Retrieve all documents from a specified collection.
        :param collection_name: The name of the collection.
        :return: A list of all documents in the collection.
        """
        # Get the collection
        collection = self.database[collection_name]

        # Retrieve all documents from the collection
        documents = list(collection.find())

        # Return the documents
        return documents

    def get_current_database(self):
        """
        Get the current database instance.
        :return: Current database instance
        """
        return self.database

    def get_mongo_collection(self, collection_name: str):
        print(collection_name)
        return self.database[collection_name]
