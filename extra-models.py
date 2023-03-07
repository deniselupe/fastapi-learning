from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    # **user_in.dict() is performing **kwargs
    # Pydantic Models have a .dict() method that returns a dict with the model's data
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

"""
    The user submits the request with a Request body like this:
    {
        "username": "UhOhOreo",
        "password": "password123",
        "email": "myoreo@gmail.com",
        "full_name": "Cookie Monster"
    }

    The Request Body is provided as the argument for async def create_user,
    and validated against the UserIn(BaseModel). 
    
    Once it passes validation, 
    user_in gets passed in as an argument to fake_save_user that also expects
    it's argument to be validated against UserIn(BaseModel). 
    
    Once validation
    for fake_save_user passes, user_in.password will be passed as an argument
    into fake_password_hasher, and the returned value will be stored on variable
    name hashed_password. 
    
    Then **user_in.dict() and hashed_password will be 
    provided as arguments to UserInDB(BaseModel).

    The value of UserInDB(**user_in.dict(), hashed_password=hashed_password)
    will be returned back to async def create_user, and set as the value of 
    variable user_saved. 

    Because @app.post("/user/", response_model=UserOut) has a response model
    for UserOut, user_saved will be validated against UserOut, and the result of
    validation will be what gets returned in the Response Body.
"""