import os
import config
import hashlib


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
        return md5_str in f.read().splitlines()


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


class KnowledgeBase:
    def __init__(self):
        self.chroma = None      # 向量数据库对象
        self.splitter = None    # 文本分割器对象

    def upload_by_str(self, data, file_name):
        """
        将传入的字符串进行向量化处理 并存入向量数据库中
        """
        pass


if __name__ == "__main__":
    md5_1 = get_string_md5("钟离")
    md5_2 = get_string_md5("温迪")
    md5_3 = get_string_md5("温迪")
    md5_4 = get_string_md5("可莉")
    print(md5_1, md5_2, md5_3, md5_4, sep='\n')

    save_md5(md5_1)
    save_md5(md5_2)
    
    print(check_md5(md5_1))  # True
    print(check_md5(md5_2))  # True
    print(check_md5(md5_3))  # True
    print(check_md5(md5_4))  # False
