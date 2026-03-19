
from fastapi import APIRouter, HTTPException, status, Path, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import datetime

from apps.config.db import SessionLocal
from apps.models.models import Todos, TodoRequestSchema, TodoResponseSchema

router = APIRouter()

# ================= DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ================= CREATE TABLES =================
Todos.metadata.create_all(bind=SessionLocal().bind)

# ================= GET ALL TODOS =================
@router.get("/", response_model=List[TodoResponseSchema])
async def get_all(db: db_dependency):
    todos = db.query(Todos).all()
    return todos

# ================= GET SINGLE TODO =================
@router.get("/{todo_id}", response_model=TodoResponseSchema)
async def get_todo(todo_id: int = Path(gt=0), db: db_dependency = db_dependency):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# ================= CREATE TODO =================
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponseSchema)
async def create_todo(db: db_dependency, todo_request: TodoRequestSchema):
    todo_model = Todos(
        **todo_request.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

# ================= UPDATE TODO =================
@router.put("/{todo_id}", response_model=TodoResponseSchema)
async def update_todo(todo_id: int = Path(gt=0), todo_request: TodoRequestSchema = None, db: db_dependency = db_dependency):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.is_completed = todo_request.is_completed
    todo_model.priority = todo_request.priority
    todo_model.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(todo_model)
    return todo_model

# ================= DELETE TODO =================
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0), db: db_dependency = db_dependency):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
    return