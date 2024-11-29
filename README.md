# FastAPI Sample Project

This is a simple FastAPI project to demonstrate its features.

## Run Locally
Install dependencies:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints
- `GET /`: Welcome message.
- `GET /users`: Retrieve all users.
- `POST /users`: Create a new user.
