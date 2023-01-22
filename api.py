from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from src import scrape

app = FastAPI()

@app.on_event("startup")
def on_startup():
    load_dotenv()

class Recipe(BaseModel):
    url: str

@app.post("/recipe")
def recipe(recipe: Recipe):
    url = scrape.notion_request(recipe.url)
    return url 


