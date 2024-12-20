# -*- coding: UTF-8 -*-
import feedparser

def fetch_rss_content(rss_url):
    # 解析 RSS Feed
    feed = feedparser.parse(rss_url)

    # 检查是否解析成功
    if feed.bozo:
        raise ValueError(f"无法解析 RSS: {feed.bozo_exception}")

    # 提取内容
    posts = []
    for entry in feed.entries:
        post = {
            "title": entry.get("title", "无标题"),
            "description": entry.get("description", "无描述"),
            "link": entry.get("link", ""),
            "published": str(entry.get("published", "未知时间")),
        }
        posts.append(post)

    return posts