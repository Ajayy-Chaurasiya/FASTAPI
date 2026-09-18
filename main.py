from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []


class Todo(BaseModel):
    id: int
    task: str
    status: bool


@app.post("/todos")
def add_todo(todo: Todo):
    todos.append(todo)

    return {
        "message": "Todo added successfully",
        "todo": todo
    }


@app.get("/todos")
def get_todos():
    return {
        "todos": todos
    }