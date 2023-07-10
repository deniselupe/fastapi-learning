"""
FastAPI allows you declare additional information and validation 
for your parameters. 

Let's take this application below as an example.

The Query Parameter 'q' is of type 'Union[str, None]' (or 'str | None' in
Python 3.10), that means that it's of type 'str' but could also be 'None', 
and indeed, the default value is 'None', so FastAPI will now it's not required.
"""

from typing import Union
from fastapi import FastAPI

app = FastAPI(root_path="/api")

@app.get("/v1/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"items_id": "Foo"}, {"items_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Additional Validation

We are going to enforce that even though 'q' is optional, whenever it is 
provided, its length doesn't exceed 50 characters.


Additional Validation: Import Query and Annotated

To achieve that, first import:
    - Query from fastapi
    - Annotated from typing (or from typing_extensions in Python below 3.9)
"""

from fastapi import Query
from typing_extensions import Annotated

@app.get("/v2/items/")
async def read_items(q: Annotated[Union[str, None], Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Use 'Annotated' in the type for the 'q' parameter

Python itself does not do anything with this Annotated. And for editors and 
other tools, the type is still 'str'.

But you can use this space in Annotated to provide FastAPI with additional 
metadata about how you want your application to behave.

The important thing to remember is that the first type parameter you pass
to Annotated is the actual type. The rest, is just metadata for other tools.

The type annotation for 'q' is 'Union[str, None]', so we'll wrap this in 
Annotated, and so the argument for 'q' becomes:

    @app.get("/v2/items")
    async def read_items(q: Annotated[Union[str, None]] = None):

Both `q: Union[str, None] = None` and `q: Annotated[Union[str, None]] = None` 
mean the same thing. 'q' is a parameter that can be a 'str' or 'None', and 
by default, it is 'None'.



Add 'Query' to 'Annotated' in the 'q' parameter

Now that we have this 'Annotated' where we can put more metadata, add 'Query' 
to it, and set the parameter 'max_length' to 50.

    @app.get("/v2/items")
    async def read_items(q: Annotated[Union[str, None], Query(max_length=50)] = None):

Notice that the default value is still 'None', so the parameter is still optional.

But now, having `Query(max_length=50)` inside of 'Annotated', we are telling FastAPI
that we want it to extract this value from the Query Parameters (this would have been 
the default anyway) and that we want to have additional validation for this value (that's
why we do this, to get the additional validation).

FastAPI will now:
    - Validate the data making sure that the max length is 50 characters
    - Shnow a clear error for the client when the data is not valid
    - Document the parameter in the OpenAPI schema path operation (so it will show 
      up in the automatic docs UI)
"""

"""
Alternative (old) Query as the default value.

Previous versions of FastAPI (before 0.95.0) required you to use 'Query' 
as the default value of your parameter, instead of putting it in 'Annotated',
there's a high chance that you will see code using it around, so it's important to 
understand. 

For new code and whenever possible, use 'Annotated' as explained above. There
are multiple advantages (explained below) and no disadvantages.

This is how you would use 'Query' as the default value of your function parameter, 
setting the parameter max_length to 50.

    from typing impoty Union'
    from fastapi import FastAPI, Query

    app = FastAPI()

    @app.get("/items/")
    async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results

As in this case (without using 'Annotated') we have to replace the default value
'None' in th function with 'Query()', we now need to set the default value with the
parameter `Query(default=None)`, it serves the same purpose of defining that default
value (at least for FastAPI).

So:
    q: Union[str, None] = Query(default=None)

...makes the parameter optional, with a default value of None, the same as:
    q: Union[str, None] = None

And in Python 3.10 and above:
    q: str | None = Query(default=None)

...makes the parameter optional, witha  default value of 'None', the same as:
    q: str | None = None

But it declates it explicitly as being a Query Parameter.

Then, we can pass more parameters to 'Query'. In this case, the 'max_length' 
paramter that applies to strings:
    q: Union[str, None] = Query(default=None, max_length=50)

This will validate the data, show a clear error when the data is not valid, 
and document the parameter in the OpenAPI schema path operation.



'Query' as the default value or in 'Annotated'

Have in mind that when using 'Query' inside of 'Annotated' you cannot use the
'default' parameter for 'Query'. Instead, use the actual default value of the 
function parameter. Otherwise, it would be inconsistent. 

For example, this is not allowed:
    q: Annotated[str Query(default="rick")] = "morty"

...because it's not clear if the default value should be "rick" or "morty".

So, you would use (preferably):
    q: Annotated[str, Query()] = "rick"

...or in older code bases you will find:
    q: str = Query(default="rick")



Advantages of 'Annotated'

Using 'Annotated' is recommended instead of the default value in function 
parameters, it is better for multiple reasons.

The default value of the function paramter is the actual default value, that's
more intuitive with Python in general.

You could call the same function in other places without FastAPI, and it would
work as expected. If there's a required parameter (without a default value), your 
editor will let you know with an error, Python will also complain if you run it 
without passing the required parameter.

When you don't use 'Annotated' and instead use the (old) default value style, 
if you call that function without FastAPI in other places, you have to remember 
to pass the arguments to the function for it to work correctly, otherwise the
values will be different from what you expect (e.g., 'QueryInfo' or something 
similar instead of 'str'). And your editor wont complain, and Python 
wont' complain running that function, only when the operations inside error out.

Because 'Annotated' can have more than one metadata annotation, you 
could now even use the same function with other tools, like Typer.



Add more validations

You can also add a paramter 'min_length':
"""

@app.get("/v3/items/")
async def read_items(
    q: Annotated[Union[str, None], Query(min_length=3, max_length=50)] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Add Regular Expressions

You can define a regular expression that the paramter should match.

In the example below, this specific regular expression checks that the 
received paramater value:
    - ^: starts with the following characters, doesn't have characters before
    - fixedquery: has the exact value 'fixedquery'
    - $: ends there, doesn't have any more characters after 'fixedquery'

If you feel lost with all these "regular expression" ideas, don't worry. They 
are a hard topic for many people. You can still do a lot of stuff without needing 
regular expressions yet.

But whenever you need them and go and learn them, know that you can already use 
them directly in FastAPI.
"""

@app.get("/v4/items")
async def read_items(
    q: Annotated[Union[str, None], Query(min_length=3, max_length=50, regex="^fixedquery$")] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Default Values

You can, of course, use default values other than 'None'.

Let's say that you want to declare the 'q' Query Parameter to have a 
'min_length' of 3, and to have a default of 'fixedquery'.

Note: 
Having a default value of any type, including 'None', makes the parameter 
optional (not required).
"""

@app.get("/v5/items")
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Make it Required

When we don't need to declare more validations or metadata, we can 
make the 'q' query parameter just by not declaring a default value, like:
    q: str

Instead of:
    q: Union[str, None] = None

But we are now declaring it with 'Query', for example like:
    q: Annotated[Union[str, None], Query(min_length=3)] = None

So, when you need to declare a value as required while using 'Query', 
you can simply not declare a default value:
    q: Annotated[str, Query(min_length=3)]

This will let FastAPI know that this parameter is required.



Required with Ellipsis(...)

There's an alternative way to explicitly declare that a value is required. 
You can set the default to the literal value ...:
    q: Annotated[str, Query(min_length=3)] = ...

If you hadn't seen that ... before: it is a special single value, it is part 
of Python and is called "Ellipsis". It is used by Pydantic and FastAPI to 
explicitly declare that a value is required.



Required with None

You can declare that a parameter can accept None, but that it's still 
required. This would force clients to send a value, even if the value is 'None'.

To do that, you can decalre that 'None' is a valid type but still use ... as the
default:
    q: Annotated[Union[str, None], Query(min_length=3)] = ...



Tip:
Pydantic, which is what powers all the data validation and serialization in FastAPI,
has a special behavior when you use 'Optional' or 'Union[Something, None]' without
a default value, you can read more about it in the Pydantic docs about 
Required Optional Fields.



Use Pydantic's 'Required' instead of Ellipsis (...)

If you feel uncomfortable using ..., you can also import and use 
'Required' from Pydantic.

Tip:
Remember that in most of the cases, when something is required, you 
can simply omit the default, so you normally don't have to use ... nor
'Required'.
"""

from pydantic import Required

@app.get("/v6/items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = Required):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Query Parameter List / Multiple Values

Whenever you define a Query Parameter explicitly with Query, 
you can also declare it to receive a list of values, or said 
in other way, to receive multiple values.

For example, to declare a Query Parameter `q` that can appear 
multiple times in the URL, you can write:
"""
from typing import List

@app.get("/v7/items/")
async def read_items(q: Annotated[Union[List[str], None], Query()] = None):
    query_items = {"q": q}
    return query_items

"""
Query Parameter List / Multiple Values Cont'd

Then, with a URL like:
http://localhost:8000/items/?q=foo&q=bar

You would receive a `q` Query Parameter's values (foo and bar) in a Python
list inside your Path Operation function, in the function parameter `q`.

Tip:
To declare a Query Parameter with a type of list, like in the example above, 
you need to explicitly use Query, otherwise it would be interpreted as a 
request body.
"""

{
    "q": [
        "foo",
        "bar"
    ]
}

"""
Query Parameter List / Multiple Values With Defaults

And you can also define a default list of values if none are provided.

With the Path Operation below, if you go to:
http://localhost:8000/items/

The default of `q` will be: `["foo", "bar"]` and your response will be:
{
    "q": [
        "foo",
        "bar"
    ]
}
"""

@app.get("/v8/items")
async def read_items(q: Annotated[List[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

"""
Using list

You can also use `list` directory instead of `List[str]` (or `list[str]`
in Python 3.9+).

Have in mind that in this case, FastAPI wont check the contents of the list.

For example, `List[int]` would check (and document) that the contents of the 
list are integers. But `list` along wouldn't.
"""

@app.get("/v9/items/")
async def read_items(q: Annotated[list, Query()] = []):
    query_items = {"q": q}
    return query_items

"""
Decalre More Metadata

You can add more information about the parameter.

The information will be included in the generated OpenAPI and used by the 
documentation user interfaces and external tools.

Note:
Have in mind that different tools might have different levels of OpenAPI
support. Some of them might not show all the extra information decalred 
yet, although in most of the cases, the missing feature is already 
planned for development.
"""

# You can add a `title`:
@app.get("/v10/items/")
async def read_items(q: Annotated[Union[str, None], Query(title="Query string", min_length=3)] = None):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results

# And a description
@app.get("/v11/items/")
async def read_items(
    q: Annotated[
        Union[str, None],
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Alias Parameters

Imagine that you want the parameter to be `item_query`.

Like in:
http://localhost:8000/items/?item-query=foobaritems

But `item-query` would not be a valid Python variable name.
The closes would be `item_query`.
But you still need it to be exactly `item-query`...
Then you can declare an `alias`, and that alias is what will be used to find the parameter value:
"""

@app.get("/v12/items/")
async def read_items(q: Annotated[Union[str, None], Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Deprecating Parameters

Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it,
but you want the docs to clearly show it as deprecated.

Then pass the parameter `deprecated=True` to `Query`:
"""

@app.get("/v13/items/")
async def read_items(
    q: Annotated[
        Union[str, None],
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^fixedquery$",
            deprecated=True
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Exclude From OpenAPI 

To exclude a Query Parameter from the generated OpenAPI schema (and 
thus, from the automatic documentation systems), set the parameter `include_in_schema`
of `Query` to `False`:
"""

@app.get("/v14/items/")
async def read_items(hidden_query: Annotated[Union[str, None], Query(include_in_schema=False)] = None):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

