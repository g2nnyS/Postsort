# -*- coding: UTF-8 -*-
import pymysql
import logging
from Modules.config_loader import ConfigLoader

def create_database_if_not_exists(db_config):
    logging.debug(f"正在检查数据库 {db_config['name']} 是否存在")
    conn = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['name']}")
    conn.close()

def insert_post(title, description, published, link, tag):
    logging.debug(f"正在插入文章: {link}")
    # 加载配置
    config_loader = ConfigLoader()
    if not config_loader.validate_config():
        raise ValueError("配置文件验证失败")

    config = config_loader.config
    db_config = config["database"]

    # 创建数据库（如果不存在）
    create_database_if_not_exists(db_config)

    # 连接数据库
    conn = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["name"]
    )
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                      (title TEXT, description TEXT, published TEXT, link TEXT, tag TEXT)''')

    if not isinstance(tag, str):
        raise TypeError("tag 应该是一个字符串")
        
    # 插入数据
    cursor.execute(
        "INSERT INTO posts (title, description, published, link, tag) VALUES (%s, %s, %s, %s, %s)",
        (title, description, published, link, tag)
    )

    conn.commit()
    conn.close()