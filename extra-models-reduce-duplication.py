from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union, List, Dict

app = FastAPI()

"""
    This is a continuation of the extra-models.py file.

    Instead of duplicating the same attributes and type declarations for 
    UserIn, UserOut, and UserInDB models, we can make a UserBase model and
    make subclasses for UserIn, UserOut, and UserInDB.

    That way, we can just declare just the differences between the models
    (with plaintext password, with hashed_password and without password).
"""


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really.")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_savee_user(user_in)
    return user_saved

# Union or anyOf
# You can declare a response to be the Union of two types, that means, that the response would be any of the two
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {
        "description": "All my friends drive a low rider",
        "type": "ship"
    },
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5
    }
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

"""
    If I submit a request with /items/item1, I will receive the response body for CarItem(BaseItem),
    if I remove the type attribute from items.item1 and submit a request again for /items/item1,
    I will still receive the response body for CarItem(BaseItem). The reason for this is because 
    items.item1 does not include a size attribute, therefore it passes validation for CarItem(BaseItem).

    For this reason, sending a request for /items/item2, you will receive the response for 
    PlaneItem(BaseItem).
"""

# List of models
# You can also declare responses of lists of objects
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"}
]

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

# Response with arbitrary dict
# You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values
# Without using a Pydantic model
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}