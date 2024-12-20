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
        return " ".join(self.response_content).split()

    def is_complete(self) -> bool:
        return self.response_complete
