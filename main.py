# -*- coding: UTF-8 -*-
import uvicorn
import pymysql
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from Modules.config_loader import ConfigLoader
from Modules.filter import start_fetching

app = FastAPI()
config_loader = ConfigLoader()
config = config_loader.config

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
    config_loader = ConfigLoader()
    config = config_loader.config
    db_config = config["database"]

    conn = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["name"]
    )
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, published, link, tags FROM posts')
    rows = cursor.fetchall()
    conn.close()

    posts = []
    for row in rows:
        posts.append(Post(
            title=row[0],
            description=row[1],
            published=row[2],
            link=row[3],
            tags=row[4].split(',')
        ))

    return posts

if __name__ == "__main__":
    threading.Thread(target=start_fetching, daemon=True).start() # 启动定时任务
    uvicorn.run(app, host=config["server"]["host"], port=config["server"]["port"])