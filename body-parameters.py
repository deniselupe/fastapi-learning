from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Union, Set

app = FastAPI()

"""
Lessons Learned:
You can add multiple body parameters to your path operation function,
even though a request can only have a single body.
"""

# Sending multiple body parameters
# In this case, FastAPI will see that there are more than one body parameter provided (2 parameters that are pydantic models)
# So then it will put both bodies inside a dict, and the parameter names will be the key names. 
# So, it will then use the parameter names as keys (field names) in the body, and expect a body that looks like:
"""
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
    }
}
"""
class Setting(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/settings/{setting_id}")
async def update_setting(setting_id: int, setting: Setting, user: User):
    results = {"setting_id": setting_id, "setting": setting, "user": user}
    return results

# Singular Values in Body Parameter
# For example, extending the previous model, you could decide that you want to have another
# key 'importance' in the same body, besides the 'item' and 'user'.

# If you declare 'importance' as-is, FastAPI will assume that it is a query parameter
# because the importance parameter is a singular value, and by default FastAPI
# assumes that a parameter is a query parameter if they are not listed in the path and have singular value (not Pydantic model, so just int, str, etc)

# But you can instruct FastAPI to treat 'importance' as another body key using Body
# Request Body should now look like the following in order for FastAPI to understand:
"""
{
  "item": {
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
  },
  "user": {
    "username": "string",
    "full_name": "string"
  },
  "importance": 0
}
"""
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# You can provide additional query parameters alongside those additional body parameters
# Keep in mind that Body also has the same extra validation and metadata parameters that Query and Path offer
@app.put("/features/{feature_id}")
async def update_feature(
    *,
    feature_id: int,
    feature: Item,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None
):
    results = {
        "feature_id": feature_id,
        "feature": feature,
        "user": user,
        "importance": importance
    }
    if q:
        results.update({"q": q})
    return results

# Embed a single body parameter
# Let's say you only have a single item body paramater from a Pydantic model Item
# By default, FastAPI will then expect its body directly
# But if you want it to expect a JSON with a key 'item' and inside of it the model contents,
# as it does when you declare extra body parameters, you can then use the special Body parameter 'embed'
"""
Because you are only providing just one Body Parameter, FastAPI will expect a body that looks like this:
{
    name: "string",
    description: "string",
    price: 0,
    tax: 0
}

However, you can tell FastAPI to require a body that looks like this instead by specifying Body(embed=True):
{
    "title": {
        name: "string",
        description: "string",
        price: 0,
        tax: 0
    }
}
"""
class Title(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/titles/{title_id}")
async def update_title(title_id: int, title: Title = Body(embed=True)):
    results = {"title_id": title_id, "title": title}
    return results

# The same way you can declare additional validation and metadata in path operation function parameters
# with Query, Path, and Body, you can declare validation and metadata inside of Pydantic models
# using Pydantic's 'Field'. You will need to import this from Pydantic.
class Book(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="The description of the book", description="The actual description", max_length=300)
    price: float = Field(gt=0, descripton="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: Book = Body(embed=True)):
    results = {"book_id": book_id, "book": book}
    return results

# You can define an attribute to be a subtype, for example, a python 'list'
# list will make tags be a list, althought it doesn't declare the type of the elements of the list
# In Python 3.6 to Python 3.9 you would need to import List from typing module to specify the type annotations for fields inside list
class Candy(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []

@app.put("/candies/{candy_id}")
async def update_candy(candy_id: int, candy: Candy):
    results = {"candy_id": candy_id, candy: candy}
    return results

# Nested Models
# We are going to use a model as a type annotation for one of the Product model's attributes
"""
The request body that FastAPI will expect is:
{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "tags": [],
  "image": {
    "url": "string",
    "name": "string"
  }
}
"""
class Image(BaseModel):
    url: HttpUrl # HttpUrl is a Pydantic exotic type, a complex singular type that inherits from str (ensures that value is valid URL)
    name: str

class Product(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    results = {"product_id": product_id, "product": product}
    return results