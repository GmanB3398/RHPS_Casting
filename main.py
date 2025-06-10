from io import StringIO

import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse

from src.classes.cast_generator import CastGenerator

app = FastAPI()


@app.get("/health")
async def health():
    return HTMLResponse(status_code=200)


@app.get("/")
async def main():
    content = """
<body>
<form action="/upload_file" enctype="multipart/form-data" method="post">
<input name="files" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/upload_file")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    contents_decoded = contents.decode()
    pd.read_csv(StringIO(contents_decoded))
    return {"filename": file.filename}


@app.post("/get_casts")
async def get_casts():
    roles = app.state.roles
    preferences = app.state.preferences
    available_members = preferences["member"].to_list()
    cg = CastGenerator(available_members, roles, preferences)
    df = cg.get_all_casts()
    return HTMLResponse(content=df.to_html(index=False), status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
