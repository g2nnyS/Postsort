# -*- coding: UTF-8 -*-
import yaml
import textwrap

class ConfigLoader:
    def __init__(self, config_path="config.yml"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"找不到配置文件: {self.config_path}")
            return None
        except yaml.YAMLError as e:
            print(f"配置文件加载错误: {e}")
            return None

    def validate_config(self):
        if not self.config:
            return False
            
        required_keys = ["api", "proxy", "server"]
        for key in required_keys:
            if key not in self.config:
                print(f"配置文件缺少必要的键: {key}")
                return False
                
        # 确保 system_prompt 是字符串类型
        if "api" in self.config and "system_prompt" in self.config["api"]:
            raw_prompt = self.config["api"]["system_prompt"]
            # 使用 dedent 处理多行字符串并确保其类型为 str
            self.config["api"]["system_prompt"] = textwrap.dedent(str(raw_prompt)).strip()
            
        return True