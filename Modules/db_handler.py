'''
Date: 2025-03-03 00:06:08
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-03-03 02:03:35
FilePath: /Postsort/Modules/db_handler.py
'''
# -*- coding: UTF-8 -*-
import pymysql
import logging
from dbutils.pooled_db import PooledDB
from Modules.config_loader import ConfigLoader

def create_pool(db_config):
    return PooledDB(
        creator=pymysql,
        maxconnections=5,
        mincached=2,
        maxcached=5,
        blocking=True,
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["name"],
        charset='utf8mb4'
    )

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

    # 创建连接池
    pool = create_pool(db_config)

    # 从连接池获取连接
    conn = pool.connection()
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