from fastapi import FastAPI, Query
from pydantic import BaseModel, Required
from typing import Union, List, Tuple
from enum import Enum

app = FastAPI()

"""
Notes about how FastAPI determines which parameter is which.

1. Path Parameter
2. Query Parameter
3. Body Parameter

If the parameter passed in matches the parameter in the decorator,
FastAPI recognizes the parameter as a Path Parameter.

If the parameter's type annotation is a Pydantic Base Model, 
FastAPI recognizes the parameter as a Body Parameter.

If teh parameter passed in does not match the parameter in the decorator,
and does not have a type annotation of a Pydantic Base Model, FastAPI
recognizes then parameter as a query parameter.
"""

# My first api
@app.get("/")
async def hello_world():
    return {"message": "hello world"}

# Python Enumeration for predefined path parameters
class ModelName(str, Enum):
    alexnet = 'alexnet'
    lenet = 'lenet'
    resnet = 'resnet'

# Path parameters and the conditional responses
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }
    
    if model_name.value == 'lenet':
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }

    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }

# Return only those indexes in fake_item_db specified by query parameters skip and limit
# /items/?skip=0&limit=10
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Mixing path parameters with optional query parameters
# FastAPI knows if a parameter is path or query
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}

    if q:
        item.update({"q": q})
    
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return item

# Mix multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id} ")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})
    
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return item


# Creating a pydantic BaseModel for post requests to "/items/"
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

# Path operation for post requests to "/items/" using request body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Path operation with request body and path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Path operation with body, path, and query parameters
@app.put("/feature/{feature_id}")
async def create_item(feature_id: int, item: Item, q: Union[str, None] = None):
    result = {"feature_id": feature_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# FastAPI allows you to declare additional infomration and validation for your parameters
@app.get("/examples/")
async def read_examples(q: Union[str, None] = None):
    results = {"examples": [{"example_id": "Foo"}, {"example_id": "Bar"}]}

    if q:
        results.update({"q": q})
    return results

# Additional validation for str query parameter types
@app.get("/justice/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Additonal vaidations with regular expressions
@app.get("/who/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50, regex='^fixedquery$')):
    results = {'items': [{'item_id': 'Foo'}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Query parameter whose default value is something other than None
@app.get("/bruh/")
async def read_items(q: str = Query(default="fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}], "q": q}
    return results

# Query parameter that is required w/Query()
@app.get("/idk/")
async def read_items(q: str = Query(min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Required query parameter using an ellipsis (...)
# ... is used by FastAPI and Pydantic to explicitly declare a parameter is required
@app.get("/tired/")
async def read_items(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Required query parameter with None
# You can declare that a parameter can accept None, but that the parameter is still required
@app.get("/another/")
async def read_items(q: Union[str, None] = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Pydantic's Required instead of using ellipsis
@app.get("/play/")
async def read_items(q: str = Query(default=Required, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Query parameter that can have multiple values and returns a list with those values
# Request: https://example/com/multiple/?q=hello&q=world&q=and&q=good&q=night
# Response: {"q":["hello","world","and","good","night"]}

# To declare a query parameter with a type of list, you need to explicitly use Query,
# otherwise it would be interpreted as a request body. The reason for this is because FastAPI
# by default interprets parameters with single values as query parameters, but in this case
# the query parameter is going to be a list which may have multiple values.
@app.get("/multiple/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    
    return results

# Query parameter list, multiple values with defaults
@app.get("/hello/")
async def read_items(q: List[str] = Query(default=["hello", "world"])):
    query_items = {"q": q}
    return query_items


# Tip: List[] does not accept more than one type annotation, so you cannot do something like List[str, int].
# You can however do something like this though if needed, List[Union[int, str]], should hopefully help.
# At the same time though, other developers recommend not doing this as they want to keep List[] a homogenous structure.

# Order matters! If you had put List[Union[str, int]], the default value of q would return as a list of strings.
# Even though you provided a int -> 3, the 3 gets converted to a string because it's the first type listed inside
# the Union. 

# So it's when you specify the Union as List[Union[int, str]] that FastAPI first checks to see if the paramater
# can be converted to a integer, and if not, then the paramter returns as a string. Therefore, a query parameter
# that looks like /alt/?q=hello&q=123 would actually return a list that is ["hello", 123] and not ["hello", "123"]
@app.get("/alt/")
async def read_items(q: List[Union[int, str]] = Query(default=["str", 3])):
    query_items = {"q": q}
    return query_items

# You can also use list directly as type annotation
# Using list alone means that FastAPI will not check the contents of the list provided
# For example, in List[str], FastAPI makes sure that all contents inside the list is a str
# But when using list alone FastAPI will not make these checks, it will only ensure there is a list
@app.get("/just/")
async def read_items(q: list = Query(default=[])):
    query_items = {"q": q}
    return query_items

# Adding metadata about a parameter, like the title and description paramters inside Query
@app.get("/metadata/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Alias parameters for your query parameters
# Lets say you need your query parameter to be ?item-query, but item-query is not a valid name for a parameter
# Still though, it's required that the parameter name is ?item-query=, this is what you can do achieve this.
# '/alias/?item-query=helloworld' will return '{"items":[{"item_id":"Foo"},{"item_id":"Bar"}],"q":"helloworld"}'
@app.get("/alias/")
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Exclude query parameter from OpenAPI
@app.get("/exclude/")
async def read_items(
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

# Show that a query parameter is deprecated
# If you still need the route running but plan on deprecating soon, this lets others know in OpenAPi that it's going away
@app.get("/deprecate/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results