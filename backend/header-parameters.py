"""
Header Parameters

You can define Header Parameters the same way you define Query, Path, and Cookie
parameters.


Import Header

First, import Header.


Declare Header Parameters

Then decalre the Header Parameters using the same structure as with 
Path, Query, and Cookie.

The first value is the default value, you can pass all the extra validation 
or annotation parameters:
"""

from typing import Union
from fastapi import FastAPI
from typing_extensions import Annotated

app = FastAPI()

@app.get("/v1/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}


"""
Technical Details

`Header` is the "sister" class of `Path`, `Query`, and `Cookie`. It 
also inherits from the same common Param class. 

But remember that when you import `Query`, `Path`, `Header`, and others 
from `fastapi`, those are actually functions that return special classes.


Info

To decalre headers, you need to use `Header`, because otherwise the parameters 
would be interpreted as query parameters.
"""

"""
Automatic Conversion

`Header` has a little extra functionality on top of what `Path`, `Query`, and `Cookie` 
provide.

Most of the standard headers are separated by a "hyphen" character, also known as the 
"minus symbol" (-).

But a variable like `user-agent` is invalid in Python.'

So, by default, `Header` will convert the parameter names characters from underscore (_) 
to hyphen (-) to extract and document the headers.

Also, HTTP headers are case-insensitive, so, you can declare them with standard 
Python style (also known as "snake_case").

So, you can use `user_agent` as you normally would in Python code, instead of needing 
to capitalize the first letters as `User_Agent` or something similar.

If for some reason you need to disable automatic conversion of underscores to hyphens, 
set the parameter `convert_underscores` of `Header` to `False`.


Warning

Before setting `convert_underscores` to `False`, bear in mind that some HTTP proxies 
and servers disallow the usage of headers with underscores.
"""

@app.get("/v2/items")
async def read_items(strange_header: Annotated[Union[str, None], Header(convert_underscores=False)] = None):
    return {"strange_header": strange_header}


"""
Duplicate Headers

It is possible to receive duplicate headers. That means, the same header with multiple 
values.

You can define those cases using a list in the type declaration.

You will receive all the values from the duplicate header as a Python `list`.

In the example below, we decalre a header of `X-Token` that can appear more than once.

If you communicate with the below Path Operation sending two HTTP headers like:
    X-Token: foo
    X-Token: bar

The response would be like:
    {
        "X-Token values": [
            "bar",
            "foo"
        ]
    }
"""

from typing import List

@app.get("/v3/items/")
async def read_items(x_token: Annotated[Union[List[str], None], Header()] = None):
    return {"X-Token values": x_token}

