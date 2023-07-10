from fastapi import FastAPI, Form
from typing_extensions import Annotated

app = FastAPI(root_path="/api")

@app.post("/login")
async def login(firstname: Annotated[str, Form()], lastname: Annotated[str, Form()], age: Annotated[int, Form()]):
    print(firstname)
    print(lastname)
    print(age)
    return {"message": f"Hello {firstname} {lastname}, you are {age} years old."}

