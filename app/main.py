from fastapi import FastAPI

from app.routers import routers

app = FastAPI(
    title="FastAPI Sample Project",
    description="A sample FastAPI project for demonstration purposes",
    version="1.0.0",
)

# Include routers
app.include_router(routers.router, prefix="")
