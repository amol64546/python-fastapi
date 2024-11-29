import logging
import os
from typing import Dict

import hvac
from fastapi import APIRouter


print(f"VAULT_HOST: {os.getenv('VAULT_HOST')}")
print(f"VAULT_TOKEN: {os.getenv('VAULT_TOKEN')}")

# Set up Vault client
client = hvac.Client(
    url=os.getenv("VAULT_HOST"),
    token=os.getenv("VAULT_TOKEN")
)


router = APIRouter()

# Check if the client is authenticated
if client.is_authenticated():
    logging.info("Connected to Vault")
else:
    print("Authentication failed")



@router.get("")
def get_secret(secret_path: str):
    try:
        secret_response = client.secrets.kv.v1.read_secret(path=secret_path)
        secret_data = secret_response['data'] # This is where the secret data lives
        print(f"Secret data: {secret_data}")
        return secret_data["GTP4O_API_KEY"]
    except Exception as e:
        print(f"Error reading secret: {e}")


@router.post("")
def set_secret(secret: Dict[str, str], secret_path: str):
    try:
        client.secrets.kv.v1.create_or_update_secret(
            path=secret_path,
            secret=secret
        )
        print("Secret written successfully")
        return secret
    except Exception as e:
        print(f"Error writing secret: {e}")
