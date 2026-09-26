from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


app = FastAPI()


# JWT settings
SECRET_KEY = "Ajay_learning_fastapi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Used to hash passwords and verify passwords
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# tokenUrl="login" means the token is obtained from /login. it extract the token from authorzation header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Fake database for storing user data.
# In a real application, this would be a real database.
users_db = {
    "Ajay": {
        "username": "Ajay",

        # Store the HASHED password, not the original password.
        "password": pwd_context.hash("Ajay1298")
    }
}


# Defines the structure of the response returned after login.
class Token(BaseModel):
    access_token: str
    token_type: str


# Defines the structure of user data.
class User(BaseModel):
    username: str


# plain_password = the original password entered by the user.
# hashed_password = the hashed password stored in the database.
def verify_password(plain_password, hashed_password):

    # Checks whether the entered password matches the stored hash.
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Finds the user and verifies their password.
def authenticate_user(username, password):

    user = users_db.get(username)

    if not user:
        return False

    # Compare entered password with stored hashed password.password is new enter password for login
    #user[password ] is old sotred hashs passwprd
    if not verify_password(password, user["password"]):
        return False

    return user


# Creates a JWT access token.
def create_access_token(data: dict):

    # Make a copy of the data we want to put inside the token.
    to_encode = data.copy()

    # Set the token expiration time.
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiration time to the JWT payload.
    to_encode.update({"exp": expire})

    # Encode/sign the data into a JWT.
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# LOGIN
@app.post("/login", response_model=Token)
def login(
# form_data contains the username$password sent byuser, oauth2requestform take data during login
    form_data: OAuth2PasswordRequestForm = Depends()
):

   
    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    # If username/password is wrong, reject the login.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Create JWT after successful authentication.
    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    # Send the JWT back to the client.
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# This function gets the current user's JWT
# from the Authorization header.
def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    # Error returned if the token is invalid.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        # Decode and verify the JWT.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get the username stored inside the token.
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Find that user in the database.
    user = users_db.get(username)

    if user is None:
        raise credentials_exception

    return user


# PROTECTED ROUTE / need jwt token for each endpoint request
@app.get("/users/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):

    # Only an authenticated user can reach this route.
    return {
        "username": current_user["username"]
    }