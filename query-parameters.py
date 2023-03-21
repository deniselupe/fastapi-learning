"""
Query Parameters

When you declare other function parameters that are not part of the
Path Parameters, they are automatically interpreted as "query"
parameters.

The query is the set of key-value pairs that go after the '?' in 
a URL, separated by '&' characters. For example, in the URL 
"http://127.0.0.1:8000/items/?skip=0&limit=10"

The Query Parameters are:
    - 'skip': with a value of 0
    - 'limit': with a value of 10

As they are part of the URL, they are "naturally" strings.

But when you declare them with Python types (in the example below, as 'int'),
they are converted to that type and validated against it.

All the same process that applied for Path Parameters also applies for Query
Parameters:
    - Editor Support
    - Data "parsing"
    - Data validation
    - Automatic documentation
"""

from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

@app.get("/v1/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

"""
Defaults

As Query Parameters are not a fixed part of a path, they can be optional
and can have default values.

In the example above they have the default values of 'skip=0' and 'limit=10'.

So, going to the URL:
    - http://127.0.0.1:8000/v1/items/

Would be the same as going to:
    - http://127.0.0.1:8000/v1/items/?skip=0&limit=10

But if you go to, for example:
    - http://127.0.0.1:8000/v1/items/?skip=20

The parameter values in your function will be:
    - skip=20: because you set it in the URL
    - limit=10: because that was the default value
"""

"""
Optional Parameters

The same way, you can declare optional query parameters, by setting 
their default to 'None'.

In the case below, the function parameter 'q' will be optional, and 
will be 'None' by default.

Also notice that FastAPI is smart enough to notice that the Path 
Parameter 'item_id' is a Path Parameter and 'q' is not, so it's
a Query Parameter.
"""
from typing import Union 

@app.get("/v1/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

"""
Query Parameter Type Conversion

You can also decalre 'bool' types, and they will be converted. 

In the case below, if you go to:
http://127.0.0.1:8000/v2/items/foo?short=1

or
http://127.0.0.1:8000/v2/items/foo?short=True

or
http://127.0.0.1:8000/v2/items/foo?short=true

or
http://127.0.0.1:8000/v2/items/foo?short=on

or
http://127.0.0.1:8000/v2/items/foo?short=yes

or any other case variations (uppercase, first letter in upppercase, etc),
your function will see the parameter short with a 'bool' value of True.
Otherwise as 'False'.
"""

@app.get("/v2/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

"""
Multiple Path and Query Parameters

You can declare multiple Path Parameters and Query Parametrs at the 
same time, FastAPI knows which is which.

And you don't have to declare them in any specific order.

They will be detected by name:
"""

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long descripton"})
    return item

"""
Required Query Parameters

When you declare a default value for Non-Path Parameters (for now, we 
have only seen Query Parameters), then it is not required.

If you don't want to add a specific value but just make it optional, 
set the default as 'None'.

But when you want to make a Query Parameter required, you can just not
declare any default value:
"""

@app.get("/v3/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

"""
Required Query Parameters Cont'd

Here the Query Parameter 'needy' is a required query parameter of
type 'str'.

If you open in your browser a URL like 'http://127.0.0.1:8000/items/foo-item'
without adding the required parameter 'needy', you will see an error like:

    {
        "detail": [
            {
                "loc": [
                    "query",
                    "needy"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

As 'needy' is a required parameter, you would need to set it in the URL:
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy

...this would work.

Return Body:

    {
        "item_id": "foo-item",
        "needy": "sooooneedy"
    }

And of course, you can define some parameters as required, some as having 
a default value, and some entirely optional.

In the case below, there are 3 Query Parameters:
    - 'needy', a required 'str'
    - 'skip', an 'int' with a default value of 0
    - 'limit', an optional 'int'
"""

@app.get("/v4/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
