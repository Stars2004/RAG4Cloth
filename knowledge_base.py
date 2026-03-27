import os
import config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    """
    检查传入的 md5 字符串是否已经被处理过

    Args:
        md5_str (str): _description_

    Returns:
        _type_: True 表示已经处理过，False 表示没有处理过
    """
    # 如果不存在 创建 md5 文件 并返回 False
    if not os.path.exists(config.md5_path):
        with open(config.md5_path, 'w', encoding='utf-8') as f:
            pass  
        return False
    
    # 如果存在 读取 md5 文件 判断 md5_str 是否在文件中
    with open(config.md5_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == md5_str:
                return True
    return False


def save_md5(md5_str: str):
    """
    将传入的 md5 字符串保存到文件中

    Args:
        md5_str (str): _description_
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """
    将传入的字符串转换为 md5 字符串

    Args:
        input_str (str): _description_
        encoding (str, optional): _description_. Defaults to 'utf-8'.

    Returns:
        _type_: _description_
    """
    md5 = hashlib.md5()
    md5.update(input_str.encode(encoding))
    return md5.hexdigest()


class KnowledgeBaseService:
    def __init__(self):
        # 确保向量数据库的存储目录存在，如果不存在则创建
        os.makedirs(config.persist_directory, exist_ok=True)

        # 向量数据库对象
        self.chroma = Chroma(
            collection_name=config.collection_name,                                 # 集合名称，相当于数据库中的 "表名"，用于区分不同的知识库      
            embedding_function=DashScopeEmbeddings(model=config.embedding_model),   # 嵌入模型 将文本转换为向量
            persist_directory=config.persist_directory,                             # 向量数据的本地存储路径，重启后数据不会丢失
        )    

        # 文本分割器对象  
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,       # 每个分块的最大长度，超过则继续分割
            chunk_overlap=config.chunk_overlap, # 相邻块之间的重叠量，保证语义连贯性
            separators=config.separators,       # 分隔符优先级列表，优先按大段落分割
            length_function=len                 # 计算文本长度的方法，这里用 len() 即按字符数
        )    

    def upload_by_str(self, data: str, file_name):
        """
        将传入的字符串进行向量化处理 并存入向量数据库中
        """
        # 获取字符串的 md5 值
        md5_str = get_string_md5(data)

        # 检查 md5 是否已经处理过，如果处理过则直接返回
        if check_md5(md5_str):
            return "[WARN] 内容已经存在于知识库中..."
        
        # 将字符串进行分割，得到文本块列表
        knowledge_chunks = self.splitter.split_text(data)   # list[str]

        # 构建元数据
        metadata = {
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin"
        }

        # 将分割后的文本块和对应的元数据添加到向量数据库中
        self.chroma.add_texts(
            knowledge_chunks, 
            metadatas=[metadata for _ in knowledge_chunks]  # list[dict] 每个文本块对应一份元数据
        )

        # 保存 md5 值到文件中，表示该内容已经处理过
        save_md5(md5_str)

        return "[SUCCESS] 内容已成功上传到知识库中..."


if __name__ == "__main__":
    kb = KnowledgeBaseService()
    result = kb.upload_by_str("这是一个测试文本，用于验证知识库的上传功能。", "testfile")
    print(result)
