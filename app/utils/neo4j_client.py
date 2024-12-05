import logging
import os

from neo4j import GraphDatabase
from neo4j.exceptions import ClientError

print(f"NEO4J_HOST: {os.getenv('NEO4J_HOST')}")
print(f"NEO4J_USERNAME: {os.getenv('NEO4J_USERNAME')}")
print(f"NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")

logger = logging.getLogger(__name__)


class Neo4jClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance of the class is created
        if cls._instance is None:
            cls._instance = super(Neo4jClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Avoid reinitializing if the instance already exists
        self.database_name = os.getenv("NEO4J_DATABASE")
        if not hasattr(self, 'driver'):
            # Initialize the driver and database connection
            # self.driver = GraphDatabase.driver(
            #     os.getenv("NEO4j_HOST"),
            #     auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
            # )
            self.driver = GraphDatabase.driver(
                "bolt://localhost:7687",
                auth=("neo4j", "oooo9999")
            )

    def ensure_database_exists(self, database_name):
        """
        Check if the specified database exists and create it if not.
        """
        with self.driver.session() as session:
            # Check if the database exists
            result = session.run("SHOW DATABASES")
            databases = [record["name"] for record in result]

            if database_name not in databases:
                print(f"Database '{database_name}' does not exist. Creating it...")
                session.run("CREATE DATABASE $db_name", db_name=database_name)
            else:
                print(f"Database '{database_name}' already exists.")

    def switch_database(self, database_name):
        """
        Switch the database for the current Neo4jClient instance.
        """
        # Ensure that the new database exists, then update the instance's database_name
        self.ensure_database_exists(database_name)
        self.database_name = database_name
        print(f"Switched to database '{self.database_name}'.")

    def get_current_database(self):
        """
        Retrieve the current database in use by the client instance.
        """
        return self.database_name

    def execute_query(self, query, parameters=None, result_transformer=None):
        """
        A generic method to execute Cypher queries on Neo4j.

        Parameters:
            - query: The Cypher query as a string.
            - parameters: Optional dictionary of parameters for the query.
            - result_transformer: Optional function to transform the result (e.g., Result.to_df).

        Returns:
            - The result of the query, possibly transformed.
        """
        if parameters is None:
            parameters = {}

        try:
            with self.driver.session(database=self.database_name) as session:
                # Execute the query
                result = session.run(query, parameters)

                # If a result transformer is provided, apply it
                if result_transformer:
                    return result_transformer(result)

                # Otherwise, return the raw result
                return result

        except ClientError as e:
            logger.error(f"Error executing query: {e}")
            if "ConstraintValidationFailed" in str(e):
                logger.warning("Entity already exists.")
            else:
                raise e
