# -*- coding: UTF-8 -*-
import yaml

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
        required_keys = ["api", "proxy", "server"]
        for key in required_keys:
            if key not in self.config:
                print(f"配置文件缺少必要的键: {key}")
                return False
        return True