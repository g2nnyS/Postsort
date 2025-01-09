<div align="center">

# Postsort
使用大语言模型的论坛帖子智能分类系统

</div>

## 这是什么？

Postsort 是一个智能论坛帖子分类系统后端，它可以：

- 🤖 使用GPT模型自动对论坛帖子进行分类
- 📊 实时抓取和处理RSS源中的新帖子
- 🏷️ 支持多种分类标签（如悬赏、出售、收购等）
- ⚡ 提供高性能的RESTful API接口

> 该项目的完整Web界面在[前端项目仓库](https://github.com/g2nnyS/Postsort_Web)

## 依赖

在开始前,请确保你的环境已安装:

- Python 3.12
- MySQL(或MariaDB)

**强烈建议**:使用虚拟环境运行

## 快速开始

配置环境:
```sh
pip install -r requirements.txt
```
修改配置文件 config.yml，设置：
- 数据库连接信息
- 任意大语言模型服务的API密钥,地址以及模型名称
- RSS源地址
- 服务器配置(如端口)

随后启动服务:
```sh
python main.py
```

## 开始使用
访问
```
http://<your-ipaddress>:<your-port>/posts
```
即可获得完整的帖子列表,以JSON格式返回