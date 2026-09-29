from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# CORS controls whether a frontend from one origin as example (http://localhost:5173) can access a
# backend API on another origin (http://localhost:8000).The backend gives permission by configuring
# CORSMiddleware and specifying allowed origins.#The browser checks and enforces this permission
# when the frontend makes the request.#If allowed, the frontend receives the response; if not, the
# browser blocks the frontend from accessing the response.
origins = [
    "http://localhost:5173"
]


# Enable CORS
app.add_middleware(
    CORSMiddleware,

    
    allow_origins=origins,# Allow requests from the frontend of port 5173

    allow_credentials=True,# Allow cookies and authentication
    allow_methods=["*"], # Allow GET, POST, PUT, DELETE, etc.

    # Allow all request headers
    allow_headers=["*"]
)


# Simple API
@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}


@app.get("/users")
def get_users():
    return {
        "users": [
            {"id": 1, "name": "Ajay"},
            {"id": 2, "name": "Ram"}
        ]
    }