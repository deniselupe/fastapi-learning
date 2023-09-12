"""
Global Dependencies

For some types of applications you might want to add dependencies to the whole
application.

Similar to the way you can add `dependencies` to the Path Operation 
Decorators, you can add them to the FastAPI application.

In that case, they will be applied to all the Path Operations in the 
application:
"""

from fastapi import Depends, FastAPI, Header HTTPException
from typing_extensions import Annotated

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

app = FastAPI (dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/v1/items/")
async def read_items():
    return [{"item": "Notebook"}, {"item": "Pens"}]

@app.get("/v1/users/")
async def read_users():
    return [{"username": "Juneau"}, {"username": "Lupe"}]

"""
And all the ideas in the section about adding `dependencies` 
to the path operation decorators still apply, but in this case, to all 
of the Path Operations in the app. 

-----

Dependencies for groups of path operations

Later, when reading about how to structure bigger applications, possibly 
with multiple files, you will learn how to declare a single `dependencies` 
parameter for a group of Parameter Operations.
"""
