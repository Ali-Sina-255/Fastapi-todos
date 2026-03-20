# servers.py
from fastapi import FastAPI

from apps.routers import auth, todos

app = FastAPI()

# Include the todos router
app.include_router(todos.router, tags=["Todos"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
