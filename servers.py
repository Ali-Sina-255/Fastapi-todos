# servers.py
from fastapi import FastAPI
from apps.routing import todos

app = FastAPI()

# Include the todos router
app.include_router(todos.router, tags=["Todos"])