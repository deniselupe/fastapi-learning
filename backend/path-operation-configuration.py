"""
Path Operation Configuration

There are several parameters that you can pass to your Path Operation decorator 
to configure it.

---

Warning

Notice that these parameters are passed directly to the 
Path Operation decorator, not to your Path Operation function.

-----

Response Status Code

You can define the (HTTP) `status_code` to be used in the response 
of your path operation. 

You can pass directly the `int` code, like 404.

But if you don't remember what each number code is for, you can 
use the shortcut constants in `status`:
"""

from typing import Set, Union
from fastapi import FastAPI, status
from pydantic import Basemodel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/v1/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

"""
That status code will be used in the response and will be added to the OpenAPI 
schema.

---

Technical Details

You could also use `from starlette import status`.

FastAPI provides the same `starlette.status` as `fastapi.status` just as a convenience 
for you, thne developer. But it comes directly from Starlette.

-----

Tags 

You can add tags to your Path Operation, pass the parameter `tags` with a `list` of `str` 
(commonly just one `str`):
"""

@app.post("/v2/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item

"""
They will be added to the OpenAPI schema and used by the automatic 
documentation interfaces.

-----

Tags with Enums

If you have a big application, you might end up accumulating several tags, 
and you would want to make sure you always use the same tag for related Path 
Operations.

In these cases, it could make sense to store the tags in an `Enum`.

FastAPI supports that the same way as with plain strings:
"""

from enum import Enum


class Tags(Enum):
    item = "items"
    users = "users"


@app.get("/v3/items/", tags=[Tags.items])
async def get_items():
    return ["Books", "Candy"]
    
@app.get("/v1/users/", tags=[Tags.users])
async def read_users():
    return ["Pancake", "Oreo"]

"""
Summary and Description

You can add a `summary` and `description`:
"""

class ItemTwo(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post(
    "/v4/items/",
    response_model=ItemTwo,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item

"""
Description from docstring

As descriptions tend to be long and cover multiple lines, you can 
declare the Path Operation description in the function docstring 
and FastAPI will read it from there.

You can write Markdown in the docstring, it will be interpreted and displayed 
correctly (taking into account docstring indentation).
"""

@app.post("/v5/items/", response_model=ItemTwo, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

"""
It will be used in the interactive docs.

-----

Response Description

You can specify the response description with the parameter 
`response_description`:
"""

@app.post(
    "/v6/items/",
    response_model=ItemTwo,
    summary="Create an item",
    resposne_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

"""
Info

Notice that `response_description` refers specifically to the response, 
the description refers to the Path Operation in general.

---

Check 

OpenAPI specifies that each Path Operation requires a response description.

So, if you don't provide one, FastAPI will automatically generate one of "Successful response".

-----

Deprecate a path operation

If you need to mark a Path Operation as deprecated, but without removing it, pass the 
parameter `deprecated`.
"""

@app.get("/v1/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

"""
It will be clearly marked as deprecated in the interactive docs.

-----

Recap You can configure and add metadata for your Path Operations 
easily by passing parameters to the Path Operation decorators.
"""