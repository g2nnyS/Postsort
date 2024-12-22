# -*- coding: UTF-8 -*-
import openai
import os
import time
import logging
from Modules.response_handler import ResponseHandler

class OpenAIHandler:
    def __init__(self, config):
        # 配置日志
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.api_key = config["api"]["api_key"]
        self.base_url = config["api"]["base_url"]
        self.model = config["api"]["model"]
        self.proxy = config["proxy"]["url"] if config["proxy"]["status"] else None
        self.system_prompt = str(config["api"]["system_prompt"]).strip()
        openai.api_key = self.api_key
        openai.base_url = self.base_url
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

        if self.proxy:
            if not isinstance(self.proxy, str):
                raise TypeError("proxy 应该是一个字符串")
            os.environ["http_proxy"] = self.proxy
            os.environ["https_proxy"] = self.proxy
            logging.info(f"状态：使用代理: {self.proxy}")
        else:
            os.environ.pop("http_proxy", None)
            os.environ.pop("https_proxy", None)
            logging.info("状态：未使用代理")

    def analyze_intent(self, user_input, retries=3):
        self.conversation_history = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_input}]
        handler = ResponseHandler()
        
        for attempt in range(retries):
            try:
                logging.info("开始等待AI响应...")
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    stream=True,
                )
                
                content_received = False
                for chunk in response:
                    try:
                        if hasattr(chunk.choices[0], 'delta'):
                            content = chunk.choices[0].delta.content
                            if content:
                                handler.add_content(content)
                                content_received = True
                        if chunk.choices[0].finish_reason == "stop":
                            if not content_received:
                                logging.warning("收到结束标志但未收到内容")
                                continue
                            handler.mark_complete()
                            logging.info("AI响应完成")
                            break
                    except AttributeError:
                        continue
                
                if handler.is_complete() and content_received:
                    result = handler.get_result()
                    if result:
                        return result
                    logging.warning("响应完成但结果为空，重试中...")
                    time.sleep(1)
                    continue
                else:
                    logging.warning("响应不完整，重试中...")
                    time.sleep(1)
                    continue
                    
            except Exception as e:
                logging.error(f"API调用错误: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                return ["未分类"]  # 发生错误时返回未分类
                
        logging.error("达到最大重试次数，返回空结果")
        return ["未分类"]  # 所有重试失败后返回未分类