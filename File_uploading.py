

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles

import os
import shutil


app = FastAPI()




# "uploads" is the actual folder name.
# UPLOAD_DIR is just a variable that stores the name/path of that folder.
UPLOAD_DIR = "uploads"


# Create the "uploads" folder if it does not already exist.
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Make the files inside the "uploads" folder accessible through a URL.
app.mount(
    "/files",                              # URL path
    StaticFiles(directory=UPLOAD_DIR),    # actual folder where files exist
    name="files"                           # name/identifier of the mounted application
)

#define a function named upload_file that receives a required uploaded file(...)from the user, 
# stores it in the variable file, #here fastAPI receives that files
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):#.treats it as a FastAPI UploadFile object.

    filename = file.filename

    # Check whether a file was selected
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected"
        )

    # Create the destination path
    #We create the complete location where the file should be saved, such as uploads/cat.jpg.
    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Create/open the destination file menas create a file if not created , if created then open
    # "wb" = write binary , buffer means as a destination location
    with open(file_path, "wb") as buffer:

#We copy the actual uploaded file data into that destination.This is why we use shutil.copyfileobj().
# Now the file is physically saved inside the uploads folder.
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Return information to the client
    return {
        "message": "File uploaded successfully",
        "filename": filename,
        "file_url": f"http://127.0.0.1.8000/files/{filename}"
    }
    
@app.get("/upload")
def get_file(filename:str):
    raise HTTPException(status_code=404,details="files not found in upload folder")

    return {
   "File_url": f"http://127.0.0.1.8000/files/{filename}"
}