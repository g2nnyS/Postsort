# -*- coding: UTF-8 -*-
import openai
import logging
import os

class OpenAIHandler:
    def __init__(self, config): #该初始化部分内容已全部移动到./config.yml文件中
        self.api_key = config["api"]["api_key"]
        self.base_url = config["api"]["base_url"]
        self.model = config["api"]["model"]
        self.proxy = config["proxy"]["url"] if config["proxy"]["status"] else None
        self.system_prompt = config["api"]["system_prompt"]
        openai.api_key = self.api_key
        openai.base_url = self.base_url
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

        if self.proxy:
            os.environ["http_proxy"] = self.proxy
            os.environ["https_proxy"] = self.proxy
            logging.info(f"状态：使用代理: {self.proxy}")
        else:
            os.environ.pop("http_proxy", None)
            os.environ.pop("https_proxy", None)
            logging.info("状态：未使用代理")

    def analyze_intent(self, user_input, retries=3):
        self.conversation_history.append({"role": "user", "content": user_input})
        for attempt in range(retries):
            try:
                # 调用远程API
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                )
                assistant_response = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
                return assistant_response
            except openai.OpenAIError as e:
                logging.error(f"OpenAI API error: {e}")
                return None
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                if attempt < retries - 1:
                    logging.info("重试中...")
                else:
                    return None