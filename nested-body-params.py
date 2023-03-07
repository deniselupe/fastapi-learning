from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Set, Dict, Union

app = FastAPI()

# Nested Models, you can list attribute types as models
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None #You can use the submodel for list with type parameter Image [{url, name}]

class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]

"""
The request body that FastAPI expects is:
{
  "name": "string",
  "description": "string",
  "price": 0,
  "items": [
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

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# Bodies of pure lists
# If the top level value of the JSON body you expect is a JSON array, you can declare
# the type in the parameter of the function, the same as Pydantic models
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


# Bodies of arbitrary dicts
# You can also declare a body as a dict with keys of some type and values of other types
# Without having to know beforehand what are the valid field/attribute names (as would be the case with Pydantic models)
# This would be useful if you want to receive keys that you don't already know
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

# Pydantic schema_extra
# You can declare an example for a Pydantic model using Config and schema_extra
# This will be the schema that is shown as the example request body in OpenAPI/SwaggerUI
class Product(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice product",
                "price": 35.40,
                "item": 3.20
            }
        }

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    results = {"product_id": product_id, "product": product}
    return results

"""
You can also use Field() by passing in an example argument to get the same schema results as above.
Just like in the example above, this would also show in the OpenAPI/SwaggerUI as the example Request Body.

class Product(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)
"""