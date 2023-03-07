from fastapi import FastAPI, Header
from typing import Union, List

app = FastAPI()

"""
    The parameter name is user_agent but that's because we can't call it User-Agent, the hyphen is invalid for parameter names.

    FastAPI is smart enough to know that when you name your Header parameter user_agent, you actually mean user-agent.
    Also, headers are case insensitive so user-agent and User-Agent is the same thing.

    Also, even though it seems like there's an option here to define what the value
    of user_agent is (str or None) I am not able to customize what the str value is.

    The query will return the actual User-Agent from the request call. Probably
    because User-Agent is one of those headers that are required, so maybe unable to modify.

    Despite trying to change the value of user_agent, this was still my response body:
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
"""
@app.get("/items")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}

"""
    I was however able to manipulte what the value of this header was, because it's a custom header.

    I set the value of my_header to "Hello world!" and this was my Reponse Body:
    {
        "My-Header": "Hello world!"
    }
"""
@app.get("/posts")
async def read_posts(my_header: Union[str, None] = Header(default=None)):
    return {"My-Header": my_header}

"""
    Duplicate Headers

    It is possible to receive multiple headers. That means, the same header with multiple values.
    You can define those cases using a list in type declaration.

    So if you send multiple header parameters like:
    X-Token: foo
    X-Token: bar

    The response would be:
    {
        "X-Token": [
            "foo",
            "bar"
        ]
    }
"""
@app.get("/books")
async def read_books(x_token: Union[List, None] = Header(default=None)):
    return {"X-Token": x_token}
