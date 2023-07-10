"""
When you need to send data from a client (let's say, a browser) to your API,
you send it as a request body.

A request body is data sent by the client to your API. A response body is the 
data your API sends to the client.

Your API almost always has to send a response body. But clients don't 
necessarily need to send request bodies all the time.

To declare a request body, you use Pydantic models with all their power and 
benefits.

To send data, you should use one of: 
    - POST (the more common)
    - PUT
    - DELETE
    - PATCH

Sending a body with a GET request has an undefined behavior in the 
specifications, nevertheless, it is supported by FastAPI, only for 
very complex/extreme use cases.

As it is discouraged, the interactive docs with Swagger UI wont 
show the documentation for the body when using GET, and proxies 
in the middle might not support it.
"""

"""
Import Pydantic's BaseModel

First, you need to import BaseModel from pydantic:

    from typing import Union
    from fastapi import FastAPI
    from pydantic import BaseModel
"""

"""
Create Your Data Model

Then you declare your data model as a class that inherits from BaseModel.

Use standard Python types for all the attributes:

    class Item(BaseModel):
        name: str
        description: Union[str, None] = None
        price: float
        tax: Union[float, None] = None

The same as when declaring Query Parameters, when a model attribute
has a default value, it is not require. Otherwise, it is required. 
Use 'None' to make it just optional.

For example, the 'Item' model above declares a JSON "object" 
(or Python 'dict') like:

    {
        "name": "Foo",
        "description": "An optional description",
        "price": 45.2,
        "tax": 3.5
    }

...as 'description' and 'tax' are optional (with a default value of 'None'), this JSON
"object" would also be valid:

    {
        "name": "Foo",
        "price": 45.2
    }
"""

"""
Declare it as a Parameter

To add it to your Path Operation, declare it in the same way you would declare
Path and Query Parameters:

    @app.post("/items/")
    async def create_item(item: Item):

...and declare its type as the model you created, 'Item'.
"""

"""
Results

With just that Python type declaration, FastAPI will:
    - Read the body of the request as JSON
    - Convert the corresponding types (if needed)
    - Validate the data
        - If the data is invalid, it will return a nice and clear error, indicating
          exactly where and what was the incorrect data.
    - Give you the received data in the parameter 'item'
        - As you declared it in the function to be of type 'Item', you will also have
          all the editor support (completion, etc) for all of the attributes and their
          types.
    - Generate JSON Schema definitions for your model, you can also use them anywhere 
      else you like if it makes sense for your project
    - Those schemas will be part of the generated OpenAPI schema, and used by the 
      automatic documention UIs
"""

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI(root_path="/api")

@app.post("/v1/items/")
async def create_item(item: Item):
    return item

"""
Endpoint: /v1/items/

Request Body:
{
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
}

Response Body:
{
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
}

Request Body:
{
    "name": "string",
    "price": 0
}

Response Body:
{
    "name": "string",
    "description": null,
    "price": 0,
    "tax": null
}
"""

@app.post("/v2/items/")
async def create_item(item: Item):
    return { "item": item }

"""
Endpoint: /v2/items/

Request Body:
{
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
}

Response Body:
{
    "item": {
        "name": "string",
        "description": "string",
        "price": 0,
        "tax": 0
    }
}

Request Body:
{
    "name": "string",
    "price": 0
}

Response Body:
{
    "item": {
        "name": "string",
        "description": null,
        "price": 0,
        "tax": null
    }
}
"""

"""
Use the model:

Inside of the function, you can access all the attributes of the 
model object directly:
"""

@app.post("/v3/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

"""
Request Body + Path Parameters

You can declare both Path Parameters and Request Body at the same time.

FastAPI will recognize that the function parameters that match Path
Parameters should be taken from the path, and that function parameters 
that are declared to be Pydantic models should be taken from the 
Request Body.
"""

@app.put("/v4/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

"""
Request Body + Path + Query Parameters

You can also decalre Body, Path, and Query Parameters, all at the 
same time.

FastAPI will recognize each of them and take the data from the 
correct place.

In the example below, the function parameters will be recognized
as follows:
    - If the parameter is also declared in the Path, it will be used as 
      a Path Parameter
    - If the parameter is of a singular type (like 'int', 'float', 'str', 'bool', etc)
      it will be interpreted as a Query Parameter
    - If the parameter is declared to be of the type of a Pydantic model, 
      it will be interpreted as a request body.

FastAPI will know that the value of 'q' is not required because of the 
default value '= None'.

The 'Union' in 'Union[str, None]' is not used by FastAPI, but will 
allow your editor to give you better support and detect errors.
"""

@app.put("/v5/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

