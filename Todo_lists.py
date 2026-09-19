from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

todos_list = []


class Todo(BaseModel):
    todo_id: int
    date: str
    task: str
    rating_of_day: int
    completed: bool


# CREATE
@app.post("/todos")
def create_todo(todo: Todo):

    todos_list.append(todo)

    return {
        "data_list": todo,
        "message": "Todo added successfully"
    }


# READ
@app.get("/todos")
def get_todos():

    return todos_list


# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):

    for index, todo in enumerate(todos_list):
        #enumerate() is a built-in Python function that lets you loop through a list while
        # getting both the index and the item at the same time.
        
        #So the todo in the for loop is initialized/assigned by the for loop itself
        #So todo is essentially a temporary variable that receives each existing Todo 
        # from todos_list one at a time.

        if todo.todo_id == todo_id:
            #At this exact moment, Python has two separate pieces of information:

            #todo_id of existing list = new id     ← ID we were searching for
            #index = 2 supposed         ← position where Python found it

            todos_list[index] = updated_todo

            return {
                "data_list": updated_todo,
                "message": "Todo updated successfully"
            }


# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for index, todo in enumerate(todos_list):

        if todo.todo_id == todo_id:

            todos_list.pop(index)

            return {
                "message": "Todo deleted successfully"
            }
             