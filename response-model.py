from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel, EmailStr

app = FastAPI()

"""
    You can declare the model used for the response with the parameter
    response_model in any of the path operations:
    - @app.get()
    - @app.post()
    - @app.put()
    - @app.delete()

    Use response_model to define response models and especially to ensure 
    private data is filtered out.

    Use the following to return only the values you want:
    - response_model_exclude_unset
    - response_model_exclude_defaults
    - response_model_exclude_none
    - response_model_exclude
    - response_model_include
"""

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

"""
    The UserIn model will be used to validate the request body data,
    and the UserOut model will be used to ensure that only certain information
    from the request body is returned back within the response body.

    In this example, UserOut will ensure that the response body excludes
    the password provided within the original request body.

    So FastAPI will take care of filtering out all the data that is not declared
    in the output model (using Pydantic).
"""

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


class Product(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


products = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

"""
    The response_model_exclude_unset path operation decorator parameter will exclude
    default values from the BaseModel provided as the response_model value. This ensures
    only values actually set are returned in the response.

    You can also use response_model_exclude_defaults and response_model_exclude_none.
    The exclude_defaults parameter excludes attributes in the pydantic model that is a
    default value (even if it was explicitly set in the request). The exclude_none
    parameter excludes attributes with the value of None.
"""
@app.get("/products/{product_id}", response_model=Product, response_model_exclude_unset=True)
async def read_products(product_id: str):
    return products[product_id]

"""
    You can also use the path operation decorator parameters:
    - response_model_include
    - response_model_exclude

    They take a set of str with the name of attributes to include 
    (omitting the rest) or to exclude (including the rest).

    This can be used as a quick shortcut if you have only one
    Pydantic model and want to remove some data from the output.

    In the below example for Ticket, the response will only return the following:
    {
        "name": "string",
        "description": "string"
    }
"""


class Ticket(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5

tickets = {
    "foo": { # {"name": "Foo", "description": null}
        "name": "Foo", 
        "price": 50.2
    },
    "bar": { # {"name": "Bar", "description": "The Bar Fighters"}
        "name": "Bar", 
        "description": "The Bar Fighters", 
        "price": 62, 
        "tax": 20.2
    },
    "baz": { # {"name": "Baz", "description": "There goes my baz"}
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5
    }
}

@app.get(
    "/tickets/{ticket_id}/name",
    response_model=Ticket,
    response_model_include={"name", "description"} # Response body will exclude every attribute in Ticket(BaseModel) except 'name' and 'description'
)
async def read_ticket_name(ticket_id: str):
    return tickets[ticket_id]

@app.get(
    "/tickets/{ticket_id}/public",
    response_model=Ticket,
    response_model_exclude={"tax"} # Response body will include every attribute in Ticket(BaseModel) except 'tax'
)
async def read_ticket_public_data(ticket_id: str):
    return tickets[ticket_id]

"""
    If you forget to use a set() when setting a reponse_model_include 
    or response_model_exclude list, FastAPI will still convert it to a 
    set() and it will work correctly.

    So setting this:
    - response_model_include=["name", "description"]

    Will be converted to this:
    - response_model_include={"name", "description"}
"""