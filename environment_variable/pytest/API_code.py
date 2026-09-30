from fastapi import FastAPI

app = FastAPI()

# API 1: Add two numbers
@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}


# API 2: Another simple API
@app.get("/message")
def message():
    return {"message": "Addition API is working"}