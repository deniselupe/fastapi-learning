from fastapi import FastAPI, Form

app = FastAPI()

"""
    When sending data from <form> fields, data is encoded as media type
    application/x-www-form-urlencoded.

    When the form includes files, the data from form fields is encoded as
    multipart/form-data.

    Otherwise, when sending request bodies that are not form fields, the
    media type application/json.

    For this reason, you cannot declare both Form parameters and Body parameters
    for the same path operation. 

    When declaring Form parameters, you will use Form(), which is a subclass of 
    Body(). Form() accepts the same parameters as Path(), Query(), and Body().

    Without using Form(), FastAPI will assume that the parameter is a Query() parameter.
"""

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}