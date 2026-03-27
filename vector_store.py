from langchain_chroma import Chroma
import config


class VectorStoreService:
    def __init__(self, embedding):
        # 嵌入模型
        self.embedding = embedding

        # 向量数据库
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """
        返回向量检索器，方便加入 chain

        Returns:
            list[Document]: _description_
        """
        # 把向量数据库变成一个可以 "根据问题找相关内容" 的工具，为后面的 LLM 提供上下文。
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_topk})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings

    # 返回向量检索器 list[Document]
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()

    # res = retriever.invoke("我的体重 180 斤，尺码推荐")
    # res = retriever.invoke("牛仔裤可以水洗吗？")
    res = retriever.invoke("冬天穿什么颜色衣服比较好看呢？")
    print(res)
