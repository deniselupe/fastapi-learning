"""
Cookie Parameters

You can define Cookie parameters the same way you define Query and Path parameters.


Import Cookie

First, import Cookie.


Decalre Cookie Parameters

Then declare the cookie parameters using the same structure as with Path and Query.
The first value is the default value, you can pass all the extra validation or annotation parameters.


Technical Details

Cookie is a "sister" class of Path and Query. It also inherits from the same common 
Param class. 

But remember that when you import Query, Path, Cookie and others from `fastapi`, 
those are actually functions that return special classes.


Info

To declare cookies, you need to use Cookie, because otherwise the parameters would 
be interpreted as query parameters.
"""

from fastapi import Cookie, FastAPI
from typing import Union
from typing_extensions import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
