"""
Body - Multiple Parameters

Now that we have seen how to use `Path` and `Query`, let's 
see more advanced uses of request body declarations.
"""

"""
Mix Path, Query, and body parameters

First, of course, you can mix `Path`, `Query` and other request body parameter
declarations freely and FastAPI will know what to do.

And you can also declare body parameters as optional, by setting 
the default to None.

Notice that in the example below, the `item` that would be 
taken from the body is optional. As it has a `None` default value.
"""

from typing import Union
from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI(root_path="/api")


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/v1/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

"""
Multiple Body Parameters

In the previous example, the Path Operations would expect a JSON body 
with the attributes of an `Item`, like:

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }

But you can also declare multiple body parameters, e.g. `item` and `user`
like in the example below.

In the case below, FastAPI will notice that there are more than 
one body parameters in the function (two parameters that are 
Pydantic models).

So, it will then use the parameter names a keys (field names) in the body, and 
expect a body like:

    {
        "item": {
            "name": "Foo",
            "description": "The Pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        }
    }


Note:
Notice that even though the `item` was declared the same way as before, 
it is now expected to be inside of the body with a key `item`.


FastAPI will do the automatic conversion from the request, so that the 
parameter `item` receives it's specific content and the same for `user`.

It will perform the validation of the compound data, and will document it 
like that for the OpenAPI schema and automatic docs.
"""


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/v2/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

"""
Singular values in body

The same way there is a `Query` and `Path` to define exdtra data for 
query and path parameters, FastAPI provides an equivalent `Body`.

For example, extending the previous model, you could decide that you want 
to have another key `importance` in the same body, besides the `item` and `user`.

If you declare it as is, because it is a singular value, FastAPI will assume that it 
is a Query Parameter.

But you can instruct FastAPI to treat it as another body key using `Body`, like in the 
example below.

In the case below, FastAPI will expect a body like:

    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    }

Again, it will convert the data types, validate, document, etc.
"""

from fastapi import Body

@app.put("/v3/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Item, 
    user: User,
    importance: Annotated[int, Body()],
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

"""
Multiple Body Params and Query

Of course, you can also declare additional Query Parameters whenever you need,
additional to any Body Parameters.

As, by default, singular values are interpreted as Query Parameters, 
you don't have to explicitly add a `Query`, you can just do:

    q: Union[str, None] = None

Or in Python 3.10 and above:

    q: str | None = None

For example:
"""

@app.put("/v4/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: Union[str, None] = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

"""
Note:
`Body` also has all the same extra validation and metadata 
parameters as `Query`, `Path` and others you will see later.
"""

"""
Embed a single body parameter

Let's say you only have a single `item` Body Parameter 
from a Pydantic model `Item`.

By default, FastAPI will then expect its body directly.

But if you want it to expect a JSON with a key `item` and inside of it 
the model contents, as it does when you declare extra Body Parameters, 
you can use the special `Body` parameter `embed`:

    item: Annotated[Item, Body(embed=True)]

An example would be below.

In the case below, FastAPI will expect a body like:

    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        }
    }

Instead of:

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
"""

@app.put("/v5/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


"""
Recap

You can add multiple Body Parameters to your Path Operation Function, 
even though a request can only have a single body.

But FastAPI will handle it, give you the correct data in your function, 
and validate and document the correct schema in the Path Operation.

You can also declare singular values to be received as part of the body.

And you can instruct FastAPI to embed the body in a key even when 
there is only a single Body Parameter declared.
"""
