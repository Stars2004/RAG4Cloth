from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import os
import json
from typing import Sequence
import config


def get_history(session_id):
    return FileChatMessageHistory(session_id, config.chat_history_path)


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, store_path):
        self.session_id = session_id    # 会话 id
        self.store_path = store_path    # 不同会话 id 的存储文件夹路径
        self.file_path = os.path.join(store_path, session_id)   # 完整的文件路径

        # 确保文件夹存在，创建 file_path 文件所在的目录
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property    # @property 装饰器将 messages 方法变成成员属性用
    def messages(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            messages_data = json.load(f)                      # 读取文件内容，得到 list[dict]
            return messages_from_dict(messages_data)    # 将 list[dict] 转换为 list[BaseMessage]
        
    def add_messages(self, messages: Sequence[BaseMessage]):
        all_messages = list(self.messages)  # 已有消息列表
        all_messages.extend(messages)       # 添加新的消息
        new_messages = [message_to_dict(message) for message in all_messages]   # 将 list[BaseMessage] 转换为 list[dict]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)  # 将 list[dict] 写入文件

    def clear(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)    # 将空列表写入文件，清空消息历史

        