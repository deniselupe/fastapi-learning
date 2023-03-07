from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import Union, List

app = FastAPI()

# Create file parameters the same way you would for Body or Form
# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}

"""
    Using UploadFile has several advantages over bytes:
    - You don't have to use File() in the default value of the parameter
    - It uses a "spooled" file (a file stored in memory up to a miximum size limit,
      and after passing this limit it will be stored in disk)
    - This means that it will work well for large files like images, videos, large binaries, 
      etc. without consuming all the memory
    - You can get metadata from the uploaded file
    - It has a file-like object async interface
    - It exposes an actual Python SpooledTemporaryFile object that you can pass directly to
      other libraries that expect a file-like object

    UploadFile Attributes:
    - filename: A str with the original file name that was uploaded (e.g. myimage.jpg)
    - content_type: A str with the content type (MIME type / media type) (e.g. image/jpeg)
    - file: A SpooledTemporaryFile (a file-like object). This is the actual Python file that 
      you can pass directly to other functions or libraries that expect a file-like object

    UploadFile Async Methods (You'll need to await them all):
    - write(data): Writes data (str or bytes) to the file
    - read(size): Reads size (int) bytes/characters of the file
    - seek(offset): Goes to the byte position offset(int) in the file
    - close(): Closes the file

"""
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


# # Optional File Uploads
# @app.post("/files/")
# async def create_file(file: Union[bytes, None] = File(default=None)):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: Union[UploadFile, None] = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}

    
# # Using UploadFile = File(...) together to get UploadFile additional metadata
# @app.post("/files/")
# async def create_file(file: bytes = File(description="A file read as bytes")):
#     return {"file_size": len(file)}



# @ app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(description="A file read as UploadFile")):
#     return {"filename": file.filename}


# # Multiple file uploads
# @app.post("/files/")
# async def create_files(files: List[bytes] = File()):
#     # list comprehension for file_sizes returned value
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)