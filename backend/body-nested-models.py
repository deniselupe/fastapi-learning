"""
Body - Nested Models

With FastAPI, you can define, validate, document, and use 
arbitrarily deeply nested models (thanks to Pydantic).
"""

"""
List Fields

You can define an attribute to by a subtype. For example, 
a Python 'list'.

In the example, below, 'list' will make 'tags' be a list, 
although it doesn't declare the type of the elements of the list.
"""

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []


@app.put("/v1/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

"""
List Fields With Type Parameter

But Python has a specific way to declare lists with internal types,
or "Type Parameters".

Importing typing's 'List'
In Python 3.9 and above you can use the standard 'list' to declare
these type annotations as we'll see below.

But in Python versions before 3.9 (3.6 and above), you first need 
to import "List" from standard Python's "typing" module.
"""

from typing import List


class ItemTwo(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.put("/v2/items/{item_id}")
async def update_item(item_id: int, item: ItemTwo):
    results = {"item_id": item_id, "item": item}
    return results

"""
Declare a 'list' with a Type Parameter

To declare types that have Type Parameters (internal types), like 'list',
'dict', 'tuple':

- If you are in a Python version lower than 3.9, import their equivalent version 
  from the 'typing' module
- Pass the internal type(s) as "Type Parameters" using square brackets: [ and ]

In Python 3.9 it would be: 
    my_list: list[str]

In versions of Python before 3.9, it would be:
    from typing import List
    my_list: List[str]

That's all standard Python syntax for type declarations.

Use the same standard syntax for model attributes with internal types.

So, in our example above, we can make 'tags' be specifically a 
"list of strings".
"""

"""
Set Types

But then we think about it, and realize that tags shouldn't repeat, 
they would probably be unique strings.

And Python has a special data type for sets of uniq items, the 'set'.

Then we can declare 'tags' as a set of strings.

With the example below, even if you receive a request with duplicate data,
it will be converted to a set of unique items.

And whenever you output that dat, even if the source had duplicates, it will 
be it will be output as a set of unique items.

And it will be annotated / documented accordingly too.
"""

from typing import Set


class ItemThree(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.put("/v3/items/{item_id}")
async def update_item(item_id: int, item: ItemThree):
    results = {"item_id": item_id, "item": item}
    return results

"""
Nested Models

Each attribute of a Pydantic model has a type. 

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific 
attribute names, types, and validations.

All that, arbitrarily nested.


Nested Models Cont'd -- Define a submodel
For example, we can define an Image model.


Nested Models Cont'd -- Use the submodel as a type
And then we can use the Image model as the type of an attribute. 


That would mean in the example below, FastAPI expects JSON body would look like this:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}


Note:
Again, doing just for declaration, with FastAPI you get:
    - Editor support (completion, etc), even for nested models
    - Data conversion
    - Data validation
    - Automatic documentation
"""


class Image(BaseModel):
    url: str
    name: str


class ItemFour(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


@app.put("/v4/items/{item_id}")
async def update_item(item_id: int, item: ItemFour):
    results = {"item_id": item_id, "item": item}
    return results

"""
Special types and validation

Apart from normal singular types like "str", "int", "float", etc. You 
can use more complex singular types that inherit from "str".

To see all the options you have, checkout the docs for "Pydantic's exotic
types". You will see some examples in the next lesson.

For example, as in the "Image" model we have a "url" field, we can declare it 
to be instead of a "str", a Pydantic's "HttpUrl".

The string will be checked to be a valid URL, and documented in JSON Schema / 
OpenAPI as such.
"""

from pydantic import HttpUrl


class ImageTwo(BaseModel):
    url: HttpUrl
    name: str


class ItemFive(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[ImageTwo, None] = None


@app.put("/v5/items/{item_id}")
async def update_item(item_id: int, item: ItemFive):
    results = {"item_id": item_id, "item": item}
    return results


"""
Attributes with lists of submodels

You can also use Pydantic models as subtypes of "list", "set", etc.

With the example below, FastAPI will expect (convert, validate, document, etc)
and JSON body like:

{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
"""


class ImageThree(BaseModel):
    url: HttpUrl
    name: str


class ItemSix(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


@app.put("/v6/items/{item_id}")
async def update_item(item_id: int, item: ItemSix):
    results = {"item_id": item_id, "item": item}
    return results

"""
Deeply Nested Models

You can define arbitrarily deeply nested models.

Notice in the example below, the Offer model has a list 
of ItemSeven objects, which in turn have an optional list of 
ImageFour objects.

FastAPI will expect a JSON body like:
{
  "name": "string",
  "description": "string",
  "price": 0,
  "item": [
    {
      "name": "string",
      "description": "string",
      "price": 0,
      "tax": 0,
      "tags": [],
      "images": [
        {
          "url": "string",
          "name": "string"
        }
      ]
    }
  ]
}
"""


class ImageFour(BaseModel):
    url: HttpUrl
    name: str


class ItemSeven(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    item: List[ItemSeven]


@app.post("/v1/offers")
async def create_offer(offer: Offer):
    return offer

"""
Bodies of pure lists

If the top level value of the JSON body you expect is a JSON
array (a Python 'list'), you can declare the type in the parameter  of the 
function, the same as in Pydantic models:

    images: List[Image]

Or in Python 3.9 and above:

    images: list[Image]

In the example below, FastAPI will expect a JSON body that looks like:
[
  {
    "url": "string",
    "name": "string"
  }
]
"""


class ImageFive(BaseModel):
    url: HttpUrl
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: List[ImageFive]):
    return images

"""
Bodies of arbitrary dicts

You can also declare a body as a 'dict' with keys of some 
type and values of other type.

Without having to know beforehand what are the valid field/attribute 
names (as would be the case with Pydantic models).

This would be useful if you want to receive keys that you don't 
already know.

Other useful cases is when you want to have keys of other type, e.g. 'int'.

That's what we are going to see here.

In this case, you would accept any 'dict' as long as it has 'int' keys 
with 'float' values.

In the example below, FastAPI expects the JSON body to look like:
{
  "1": 0,
  "2": 0,
  "3": 0
}


Tip:
Have in mind that JSON only supports "str" as keys.
But Pydantic has automatic data conversion.

This means that, even though your API clients can only send strings as keys,
as long as those strings contain pure integers, Pydantic will conver them and validate
them.

And the 'dict' you receive as 'weights' in the example below will actually have 'int' 
keys and 'float' values.
"""

from typing import Dict

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights