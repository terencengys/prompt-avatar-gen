# This script holds the REST API for selecting the prompts
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import configparser

from prompt_builder import get_themes_list, build_prompt

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
    prompt = build_prompt(create_prompt.gender, create_prompt.theme)
    return prompt


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=LOCAL_SERVER_PORT)