# -*- coding: UTF-8 -*-
import uvicorn
import pymysql
import threading
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from Modules.config_loader import ConfigLoader
from Modules.filter import start_fetching
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 加载配置
config_loader = ConfigLoader()
if not config_loader.validate_config():
    raise ValueError("配置文件验证失败")

#配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

config = config_loader.config

class Post(BaseModel):
    id: int
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

        # 给查询结果添加行号作为 id
        return [
            Post(
                id=idx + 1,  # 行号作为 id
                title=row[0],
                description=row[1],
                published=row[2],
                link=row[3],
                tag=row[4].strip()
            )
            for idx, row in enumerate(rows)
        ]
    except Exception as e:
        logging.error(f"获取帖子列表时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库查询失败")

if __name__ == "__main__":
    # 配置日志
    log_level = config["logging"]["level"]
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 设置所有模块的日志级别
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level))
    
    # 单独设置某些模块的日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)  # 抑制 httpx 的请求日志
    logging.getLogger("uvicorn").setLevel(logging.WARNING)  # 抑制 uvicorn 的请求日志
    
    threading.Thread(target=start_fetching, daemon=True).start() # 启动定时任务
    uvicorn.run(app, host=config["server"]["host"], port=config["server"]["port"])