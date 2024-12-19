# -*- coding: UTF-8 -*-
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from Modules.filter import filter_posts
from Modules.config_loader import ConfigLoader

app = FastAPI()
config = ConfigLoader().load()

class Post(BaseModel):
    title: str
    description: str
    published: str
    link: str
    tags: List[str]

@app.get("/")
def read_root():
    return {"message": "Postsort Status: OK✔"}

@app.get("/posts", response_model=List[Post])
def get_posts():
    try:
        filtered_posts = filter_posts()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    posts = [Post(
        title=post["title"],
        description=post["description"],
        published=post["published"],
        link=post["link"],
        tags=post["tags"]
    ) for post in filtered_posts]

    return posts

if __name__ == "__main__":
    uvicorn.run(app, host=config["server"]["host"], port=config["server"]["port"])