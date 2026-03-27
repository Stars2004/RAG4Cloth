# md5
md5_path = './md5.txt'

# Chroma
collection_name = 'rag'
persist_directory = './chroma_db'

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]

# topk
similarity_topk = 1

# model
embedding_model = "text-embedding-v4"
chat_model = "qwen3-max"
