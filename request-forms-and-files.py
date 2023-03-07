from fastapi import FastAPI, Form, File, UploadFile
from typing import List

app = FastAPI()

# You can define File and Form fields at the same time
@app.post("/files/")
async def create_file(file1: UploadFile = File(...), file2: UploadFile = File(...), token: str = Form()):
    print(file1.filename)
    print(file2.filename)
    print(token)
