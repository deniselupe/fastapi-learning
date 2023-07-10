from fastapi import FastAPI

app = FastAPI()

"""
You can declare path "parameters" or "variables" with the same syntax used 
by Python format strings.

The value of the path parameter item_id will be passed to you function as 
the argument item_id.

So if you run this example and go to http://127.0.0.1:8000/v1/items/foo, 
you will see a response of {"item_id": "foo"}
"""
@app.get("/v1/items/{item_id}")
async def read_items(item_id):
    return {"item_id": item_id}

"""
Path parameters with types

You can declare the type of a path parameter in the function,
using standard Python type annotations.

In this case, 'item_id' is declared to be an 'int': 
"""
@app.get("/v2/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

"""
Data Conversion

If you run the example above and open your brower at http://127.0.0.1:8000/v2/items/3, 
you will see a response of {"item_id": 3}.

Notice that the value your function received (and returned) is 3, as a
Python 'int', not a string "3". 

So with that type declaration, FastAPI gives you automatic request "parsing".
"""

"""
Data Validation


If you go to the browser and visit http://127.0.0.1:8000/v2/items/foo, you will
see an HTTP erro that says:

{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}

The error is because the Path Parameter "item_id" had a value of "foo" which is not an int.

The same error would appear if you provided a "float" instead of an "int":
http://127.0.0.1:8000/v2/items/4.2

So with the same Python type declaration, FastAPI gives you data validation.
Notice that the error also clearly states exactly the point where the validation
didn't pass.

This is incredibly helpful while developing and debugging code that interacts with 
your API.
"""

"""
Order Matters

When creating Path Operations, you can find situations where you have a 
fixed path.

Like "/users/me", let's say that it's to get data about the current user. 

And then you can also have a path "/users/{user_id}" to get data about a 
specific user by some user ID. 

Because Path Operations are evaluated in order, you need to make sure that 
the path for "/users/me" is declared before the one for "/users/{user_id}".

Otherwise, the path for "/users/{user_id}" would match also for "/users/me",
"thinking" that it's receiving a parameter "user_id" with a value of "me".
"""

@app.get("/users/me")
async def read_user_mee():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

"""
Order Matters Cont'd

Similarly, you cannot redefine a Path Operation.

In the example below, the first one define will 
always be used since the path matches first.
"""

@app.get("/users")
async def read_users():
    return ["Nigel", "Chewy"]

@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

"""
Predefined Values

If you have a Path Operation that receives a Path Parameter,
but you want the possible valid Path Parameter values to be 
predefined, you can use a standard Python Enum.

--------------

Predefined Values -> Create an Enum class

Import 'Enum' and create a sub-class that inherits from 'str'
and from 'Enum'.

An Enum is a set of symbolic names bound to unique values. They 
are similar to global variables, but they offer a more useful 
repr(), grouping, type-safety, and a few other features. They 
are most useful when you have a variable that can take one of 
a limited selection of values.

By inheriting from 'str' the API docs will be able to know that 
the values must be of type 'string' and will be able to render 
correctly.

Then create class attributes with fixed values, which will be 
the available valid values:


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

--------------

Predefined Values -> Declare a Path Parameter

Then create a Path Parameter with a type annotation using the 
enum class you created (ModelName):

    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

    
    @app.get("/models/{model_name})
    async def get_model(model_name: ModelName):

--------------

Predefined Values -> Working with Python enumerations

The value of the Path Parameter will be an enumeration member.

--------------

Predfined Values -> Working with Python Enumerations -> Compare enumation members

You can compare it with the enumberation member in your 
created enum 'ModelName':


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

    
    @app.get("/models/{model_name})
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep learning FTW"}




What happens when you annotate the 'model_name' Path Parameter as type 'ModelName'?

In the get_model function, the 'model_name' parameter is annotated with the 
'ModelName' class, which is a subclass of the 'str' type and an 'Enum object. 
This means that 'model_name' should be a string that matches one of the values 
defined in the 'ModelName' enum.

When a request is made to the "/models/{model_name}" endpoint, FastAPI will 
automatically convert the path parameter {model_name} into a 'ModelName' object 
based on the definition of the 'ModelName' enum.

If the requested 'model_name' string matches one of the values defined in the 'ModelName' 
enum, FastAPI will return a corresponding 'ModelName' object. Otherwise, FastAPI will 
raise a '422 Unprocessable Entity' error with a message indicating that the value is not 
a valid 'ModelName'.

This is the benefit of using 'Enum' in FastAPI path parameters, as it provides built-in 
validation and converts the incoming string value to a specific 'Enum' object. So, the 
'model_name' parameter in the 'get_model' function is guaranteed to be a valid 
'ModelName' object, which allows us to use it safely in our code.




What is the difference between checking if 'model_name' is 'ModelName.alexnet' 
versus checking if 'model_name' == 'ModelName.alexnet.value'?

The main difference between 'model_name is ModelName.alexnet' and 
'model_name == ModelName.alexnet.value' is the type of comparison being performed.

'model_name is ModelName.alexnet' checks whether the 'model_name' parameter is the 
alexnet object defined in the 'ModelName' enum. This comparison is based on object 
identity and checks whether the two objects are the same object in memory.

On the other hand, 'model_name == ModelName.alexnet.value' checks whether the value attribute 
of the 'model_name' object (which is a string) is equal to the string value of the alexnet option 
in the 'ModelName' enum. This comparison is based on value equality and checks whether the two 
strings have the same characters.

In the specific example provided, the two comparisons are equivalent because the alexnet option 
in the 'ModelName' enum has a string value of "alexnet". Therefore, the value attribute of the 
'model_name' object is equal to "alexnet", which is the string value of 'ModelName.alexnet'.

However, in general, these two comparisons can be different if the 'ModelName' enum options 
have different string values. In that case, 'model_name is ModelName.alexnet' would check 
for object identity, while 'model_name == ModelName.alexnet.value' would check for string 
value equality.

--------------

Predefined Values -> Working with Python Enumerations -> Get the enumeration value

You can get the actual value (a 'str' in this case) using
'model_name.value', or in general, 'your_enum_number.value':


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

    
    @app.get("/models/{model_name})
    async def get_model(model_name: ModelName):
        if model_name is ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep learning FTW"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}


Tip: You could also access the value "lenet" with 'ModelName.lenet.value'

--------------

Predefined Values -> Working with Python enumerations -> Return enumeration members

You can return enum members from your Path Operation, even nested
in a JSON body (e.g., a 'dict').

They will be converted to their corresponding values (strings in this case)
before returning them to the client.

In your client you will get a JSON response like:

    {
        "model_name": alexnet
        "message": "Deep Learning FTW!"
    }
"""

from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning FTW!"}
    
    if model_name.value  == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

"""
Path Parameters Containing Paths

Let's say you have a Path Operation with a path "/files/{file_path}".
But you need 'file_path' itself to contain a path, like "home/johndoe/myfile.txt".

So, the URL for that file would be something like "/files/home/johndoe/myfile.txt".

--------------

Path Parameters Containing Paths -> OpenAPI Support

OpenAPI doesn't support a way to decalre a Path Parameter to contain a 
path inside, as that could lead to scenarios that are difficult to test and
define.

Nevertheless, you can still do it in FastAPI, using one of the internal tools
from Starlette.

And the docs would still work, although not adding any documentation telling
that the parameter should contain a path.

--------------

Path Parameters Containing Paths -> Path Converter

Using an option directly from Starlette you can declare a Path Parameter
containing a path using a URL like "/files/{file_path: path}".

In this case, the name of the parameter is 'file_path', and the last part
':path', tells it that the parameter should match any path.

So you can use it with:

        @app.get("/files/{file_path:path}")
        async def read_file(file_path: str):
            return {"file_path": file_path}

You could need the parameter to contain "/home/johndoe/myfile.txt", with 
a leading slash (/).

In that case, the URL would be: "/files//home/johndoe/myfile.txt", with a
double slash (//) between "files" and "home".
"""

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

"""
Recap

With FastAPI, by using short, intuitive and standard Python type
declarations, you get:
    - Editor Support: error checks, autocomplete, etc.
    - Data "Parsing"
    - Data Validation
    - API annotation and automatic documentation

And you only have to declare them once.

That's probably the main visible advantage of FastAPI compared to alternative
frameworks (apart from the raw performance).
"""