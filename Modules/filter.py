import time
import logging
import threading
from Modules.config_loader import ConfigLoader
from Modules.rss_fetcher import fetch_rss_content
from Modules.api_handler import OpenAIHandler
from Modules.db_handler import insert_post

def fetch_and_store_posts():
    try:
        # 加载配置
        config_loader = ConfigLoader()
        if not config_loader.validate_config():
            raise ValueError("配置文件验证失败")

        config = config_loader.config
        rss_url = config["rss"]["url"]
        openai_handler = OpenAIHandler(config)
        
        while True:
            try:
                rss_posts = fetch_rss_content(rss_url)
                
                for post in rss_posts:
                    title = post["title"]
                    description = post["description"]
                    published = post["published"]
                    link = post["link"]
                    
                    logging.info(f"开始处理文章: {link}")
                    user_input = f"标题: {title}\n描述: {description}"
                    
                    try:
                        # 等待 AI 响应完成
                        tags = openai_handler.analyze_intent(user_input)
                        tag = tags[0] if tags else "未分类"
                        
                        if tag != "未分类":
                            insert_post(title, description, published, link, tag)
                            logging.info(f"成功处理文章: {link} -> {tag}")
                        else:
                            logging.info(f"文章被标记为未分类: {link}")
                        
                        # 确保完全处理完一条后再处理下一条
                        time.sleep(3)
                            
                    except Exception as e:
                        logging.error(f"处理文章失败: {link} - {str(e)}")
                        time.sleep(3)
                        continue
                
                time.sleep(60)  # 每分钟抓取一次
                
            except Exception as e:
                logging.error(f"抓取过程出错: {str(e)}")
                time.sleep(60)  # 发生错误时等待一分钟后重试
                continue
    except Exception as e:
        logging.critical(f"主线程出错: {str(e)}")
def start_fetching():
    thread = threading.Thread(target=fetch_and_store_posts, daemon=True)
    thread.start()
    return thread