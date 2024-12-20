# -*- coding: UTF-8 -*-
import time
import threading
from Modules.config_loader import ConfigLoader
from Modules.rss_fetcher import fetch_rss_content
from Modules.api_handler import OpenAIHandler
from Modules.db_handler import insert_post

def fetch_and_store_posts():
    # 加载配置
    config_loader = ConfigLoader()
    if not config_loader.validate_config():
        raise ValueError("配置文件验证失败")

    config = config_loader.config
    rss_url = config["rss"]["url"]
    if not rss_url:
        raise ValueError("配置文件中没有提供 RSS URL")

    # 获取 RSS 内容
    try:
        rss_posts = fetch_rss_content(rss_url)
    except ValueError as e:
        raise ValueError(f"获取 RSS 内容失败: {e}")

    # 初始化 OpenAIHandler
    openai_handler = OpenAIHandler(config)

    # 对每个帖子进行分类并添加标签
    for post in rss_posts:
        title = post["title"]
        description = post["description"]
        user_input = f"标题: {title}\n描述: {description}"
        tags = openai_handler.analyze_intent(user_input)
        if not isinstance(tags, list):
            tags = [tags]
        tags = [tag if tag is not None else '' for tag in tags]
        published = post["published"]
        link = post["link"]

        # 存储到数据库
        insert_post(title, description, published, link, tags)

def start_fetching():
    while True:
        fetch_and_store_posts()
        time.sleep(60)

# 启动定时任务
threading.Thread(target=start_fetching, daemon=True).start()