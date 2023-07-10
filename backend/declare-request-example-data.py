"""
Declare Request Example Data

You can declare examples of the data your app can receive.
Here are several ways to do it.


Pydantic "schema_extra"

You can declare an example for a Pydantic model using 'Config' and 
'schema_extra', as described in Pydantic's docs: "Schema Customization".

In the example below, the extra info will be added as-is to the output 
JSON Schema for that model, and it will be used in the API docs.

Tip:
You could use the same technique to extend the JSON Schema and add 
your own custom extra info. For example, you could use it to add metadata 
for a frontend user interface, etc.
"""

from typing import Union 
from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI(root_path="/api")


class Item(BaseModel):
    name: str 
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

    
@app.put("/v1/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

"""
Field additional arguments

When using Field() with Pydantic models, you can also declare extra info 
for the JSON Schema by passing any other arbitrary arguments to the function.

You can use this to add 'example' for each field.


Warning:
Keep in mind that those extra arguments passed won't add any validation, 
only extra information, for documentation purposes.
"""

from typing_extensions import Annotated
from pydantic import Field 


class ItemTwo(BaseModel):
    name: Annotated[str, Field(example="Foo")]
    description: Annotated[Union[str, None], Field(example="A very nice Item")] = None
    price: Annotated[float, Field(example=35.4)]
    tax: Annotated[Union[float, None], Field(example=3.2)] = None


@app.put("/v2/items/{item_id}")
async def update_item(item_id: int, item: ItemTwo):
    results = {"item_id": item_id, "item": Item}
    return results

"""
example and examples in OpenAPI

When using any of: Path(), Query(), Header(), Cookie(), Body(), Form(), File()

You can also declare a data 'example' or a group of 'examples' with additional 
information that will be added to OpenAPI.



Body with 'example'

Here we pass an 'example' of the data expected in Body():
"""

from fastapi import Body 


class ItemThree(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/v3/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Annotated[
        Item, 
        Body(
            example={
                "name": "Foo", 
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        )
    ]
):
    results = {"item_id": item_id, "item": item}
    return results

"""
Examples in the Docs UI

With any of the methods above it would look like this in the /docs:
{
  "name": "Foo",
  "description": "A very nice Item",
  "price": 35.4,
  "tax": 3.2
}

All three methods lead to the same example JSON that can be used to text
endpoints in /docs like SwaggerUI for example.
"""

"""
Body with multiple examples

Alternatively to the single 'example', you can pass 'examples' 
using a 'dict' with multiple examples, each with extra information that will 
be added to OpenAPI too.

The keys of the 'dict' identify each example, and each value is another 'dict'.

Each specific example 'dict' in the 'examples' can contain:
- 'summary': short description for the example
- 'description': A long description that can contain Markdown text
- 'value': This is the actual example shown, e.g. a 'dict'
- 'externalValue': alternative to 'value', a URL pointing to the example. Although 
  this might not be supported by as many tools as 'value'.
"""


class ItemFour(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/v4/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Annotated[
        ItemFour,
        Body(
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2
                    }
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            }
        )
    ]
):
    results = {"item_id": int, "item": ItemFour}
    return results