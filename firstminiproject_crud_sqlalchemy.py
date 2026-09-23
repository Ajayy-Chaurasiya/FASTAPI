from sqlalchemy import create_engine, Column, Integer, Boolean, String
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

#Use the SQLite database stored in the Ajay.db file in the current directory.
database_url = "sqlite:///./Ajay.db"

#sqlalchemy will create a engine which know how to conn/communicate with your database
#enggine ke through hamne db connect kara
engine = create_engine(database_url, connect_args={"check_same_thread": False})

#sessionmaker will create sessionfactory and that factory is setup with given engine
#sessionlocal ke through hamne db me operation kar sakte hai
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#sessionlocal is a sessionfactory which know how to create a session configured with this engine

#model bananke liye hamne base dediya
#Baseisa SQLAlchemy base class usedto create ORMmodel classes,this class is created by declarative_base()

Base = declarative_base()


#this is database Model
class Todo(Base):
    __tablename__ = "todos_list"
    id = Column(Integer, primary_key=True, index=True)
    work_title = Column(String)
    day = Column(String)
    completed = Column(Boolean, default=False)


# Create the tables defined in our models inside the Ajay.db database
Base.metadata.create_all(bind=engine)


#this will check in every api that there is db session or not
def get_db():  #Its purpose is to provide a database Session whenever an API endpoint needs one
    db = SessionLocal()  #Call the factory and create a new Session object, which is db
    try:
        yield db  #Give the Session object to whoever is using get_db(), while keeping this function paused.
    finally:  #Run this code when the dependency is finished, even if an error occurs.
        db.close()


@app.post("/todos")
def create_todo(
    id: int,
    work_title: str,
    day: str,
    completed: bool = False,
    db: Session = Depends(get_db)
):
    #db: Session is there because create_todo() needs a Session object to perform database operations
    # such as add() and commit().

    # Create ORM object
    todo = Todo(
        id=id,
        work_title=work_title,
        day=day,
        completed=completed
    )

    #you are creating one Todo object, which represents one row that you want
    # to put into the database.

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


@app.get("/todos")
def get_todos(
    db: Session = Depends(get_db)
):

    todos = db.query(Todo).all()  #Ask for Todo records → give me all of them.

    return todos


@app.get("/todos/{todo_id}")
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()  #Give me the first matching record from Todo with this specific ID.
    )

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    work_title: str,
    day: str,
    completed: bool,
    db: Session = Depends(get_db)
):

    # Find the todo
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    # If todo doesn't exist
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Update values
    todo.work_title = work_title
    todo.day = day
    todo.completed = completed

    db.commit()

    # Refresh object
    db.refresh(todo)

    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    # Find todo
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )

    # If todo doesn't exist
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Delete todo
    db.delete(todo)

    # Save changes
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }