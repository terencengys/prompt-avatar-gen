# This script holds the REST API for selecting the prompts
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import Response
import configparser

from prompt_builder import get_themes_list, send_prompt, send_prompt_with_img

config = configparser.ConfigParser()
config.read('config.ini')

LOCAL_SERVER_PORT = config.getint('Server', 'LOCAL_SERVER_PORT')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://0.0.0.0:{LOCAL_SERVER_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreatePrompt(BaseModel):
    gender: str
    theme: str

@app.get("/")
# Root endpoint
async def read_root():
    return {"Hello": "World"}

@app.get("/themes")
# Get list of available themes
async def get_themes():
    return get_themes_list()

@app.post("/create")
# Post to create avatar
async def create_avatar(create_prompt: CreatePrompt):
    output = send_prompt(create_prompt.gender, create_prompt.theme)
    return Response(content=output, media_type="image/png")

@app.post("/create-from-img")
# Post to create avatar from image
async def create_avatar_from_img(gender: str, theme: str, image: UploadFile=File(None)):
    output = send_prompt_with_img(gender, theme, image)
    return Response(content=output, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=LOCAL_SERVER_PORT)