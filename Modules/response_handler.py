from typing import List

class ResponseHandler:
    def __init__(self):
        self.response_complete = False
        self.response_content = []

    def mark_complete(self):
        self.response_complete = True

    def add_content(self, content: str):
        self.response_content.append(content)

    def get_result(self) -> List[str]:
        if not self.response_complete:
            return []
        
        valid_tags = ["悬赏", "出售", "收购", "情报", "曝光", "求助", "抽奖", "未分类"]
        result = "".join(self.response_content).strip()
        
        # 确保结果是有效的标签
        if result in valid_tags:
            return [result]
        return ["未分类"]

    def is_complete(self) -> bool:
        return self.response_complete
