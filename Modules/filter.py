# -*- coding: UTF-8 -*-
from Modules.config_loader import ConfigLoader
from Modules.rss_fetcher import fetch_rss_content
from Modules.api_handler import OpenAIHandler

def filter_posts():
    # 加载配置
    config_loader = ConfigLoader()
    if not config_loader.validate_config():
        raise ValueError("配置文件验证失败")

    config = config_loader.config
    rss_url = config.get("rss_url")
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
    filtered_posts = []
    for post in rss_posts:
        title = post["title"]
        description = post["description"]
        user_input = f"标题: {title}\n描述: {description}"
        tags = openai_handler.analyze_intent(user_input)
        filtered_post = {
            "title": title,
            "description": description,
            "published": post["published"],
            "link": post["link"],
            "tags": tags
        }
        filtered_posts.append(filtered_post)

    return filtered_posts