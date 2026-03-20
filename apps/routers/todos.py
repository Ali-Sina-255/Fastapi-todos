from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from apps.auth.utils import get_current_user
from apps.config.db import SessionLocal
from apps.models.models import Todos
from apps.models.schema import TodoRequestSchema, TodoResponseSchema

router = APIRouter()


# ================= DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# ================= CREATE TABLES =================
Todos.metadata.create_all(bind=SessionLocal().bind)


# ================= GET ALL TODOS =================
@router.get("/", response_model=List[TodoResponseSchema])
async def get_all(user: user_dependency, db: db_dependency):
    # todos = db.query(Todos).filter(Todos.owner == user["user_id"]).all()
    todos = db.query(Todos).filter(Todos.owner == user.id).all()
    return todos


# ================= GET SINGLE TODO =================
@router.get("/{todo_id}", response_model=TodoResponseSchema)
async def get_todo(todo_id: int = Path(gt=0), db: db_dependency = db_dependency):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# ================= CREATE TODO =================
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=TodoResponseSchema
)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequestSchema
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is Failed"
        )
    todo = Todos(
        **todo_request.model_dump(),
        owner=user.get("user_id"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# ================= UPDATE TODO =================
@router.put("/{todo_id}", response_model=TodoResponseSchema)
async def update_todo(
    todo_id: int = Path(gt=0),
    todo_request: TodoRequestSchema = None,
    db: db_dependency = db_dependency,
):
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
