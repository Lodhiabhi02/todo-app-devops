from fastapi import APIRouter, HTTPException
from ..models import Todo
from ..database import todo_collection
from bson import ObjectId

router = APIRouter(prefix="/todos", tags=["Todos"])

def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "completed": todo["completed"]
    }

@router.get("/")
async def get_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append(todo_serializer(todo))
    return todos

@router.post("/")
async def create_todo(todo: Todo):
    result = await todo_collection.insert_one(todo.dict())
    new_todo = await todo_collection.find_one({"_id": result.inserted_id})
    return todo_serializer(new_todo)

@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    result = await todo_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": todo.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated = await todo_collection.find_one({"_id": ObjectId(id)})
    return todo_serializer(updated)

@router.delete("/{id}")
async def delete_todo(id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
