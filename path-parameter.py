from fastapi import FastAPI, Path, Query
from typing import Union, List
from pydantic import BaseModel

app = FastAPI()

# You can declare the same type of validations and metadata used in Query for your Path Parameters
# You can do this for Path parameters using Path which you import from fastapi module
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Imagine you have a query parameter q as a required str value, and a Path parameter that has a default value
# Python complains if you list a parameter with a default value first before a parameter with no default value
# You can reorder the parameters so that the q parameter (the query parameter without a default value) comes first 
# before the Path parameter that does have a default value.

# FastAPI will know which parameter is for what due to their names, types, and default declarations provided like Query or Path.
# In this case, item_id matches in the pathname and also has a default Path declaration, therefore we know it's a Path parameter.
# The q parameter we know it's a query paramter because it's type hint is str and not a Pydantic model or model like List[].

# Error when declaring parameter with default value before paramater with no default:
# SyntaxError: non-default argument follows default argument
@app.get("/users/{user_id}")
async def read_items(q: str, user_id: int = Path(title="The ID of the user to get")):
    results = {"user_id": user_id}
    if q:
        results.update({"q": q})
    return results

# You can either move the parameter with the default value last, or you can just pass * as the first parameter to avoid this SyntaxError.
# This way you can pass the paramters with default values first before the parameters without default values
@app.get("/features/{feature_id}")
async def read_items(*, feature_id: int = Path(title="The ID of the feature to get"), q: str):
    results = {"feature_id": feature_id}
    if q:
        results.update({"q": q})
    return results

# Number Validations: Greater Than or Equal to with ge=
# In this example, the value of the day_id parameter needs to be greater than or equal to 1
@app.get("/days/{day_id}")
async def read_items(*, day_id: int = Path(ge=1), q: str):
    results = {"day_id": day_id}
    if q:
        results.update({"q": q})
    return results

# Number Validations: You can also do validation with gt (Greather Than) and le (Less Than or Equal to)
@app.get("/nights/{night_id}")
async def read_items(*, night_id: int = Path(gt=0, le=1000), q: str):
    results = {"night_id": night_id}
    if q:
        results.update({"q": q})
    return results


# You can mix Path, Query, and body parameters
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *, 
    item_id: int = Path(ge=0, le=1000), 
    q: Union[str, None] = None, 
    item: Union[Item, None] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results



