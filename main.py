# -*- coding: UTF-8 -*-
import uvicorn
import pymysql
import threading
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from Modules.config_loader import ConfigLoader
from Modules.filter import start_fetching

app = FastAPI()

# 加载配置
config_loader = ConfigLoader()
if not config_loader.validate_config():
    raise ValueError("配置文件验证失败")

config = config_loader.config

class Post(BaseModel):
    title: str
    description: str
    published: str
    link: str
    tag: str

@app.get("/")
def read_root():
    return {"message": "Postsort Status: OK✔"}

@app.get("/posts", response_model=List[Post])
def get_posts():
    try:
        db_config = config["database"]
        conn = pymysql.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["name"]
        )
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, published, link, tag FROM posts ORDER BY published DESC')
        rows = cursor.fetchall()
        conn.close()

        return [
            Post(
                title=row[0],
                description=row[1],
                published=row[2],
                link=row[3],
                tag=row[4].strip()
            )
            for row in rows
        ]
    except Exception as e:
        logging.error(f"获取帖子列表时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库查询失败")

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)  # 抑制 httpx 的请求日志
    
    threading.Thread(target=start_fetching, daemon=True).start() # 启动定时任务
    uvicorn.run(app, host=config["server"]["host"], port=config["server"]["port"])