from vector_store import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class RagService:
    def __init__(self):
        # 向量数据库服务 - 根据用户问题检索相关资料
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model)
        )

        # 提示词模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "根据提供的资料，简洁和专业地回答用户提问，参考资料: \n{context}"),
            ("user", "请回答用户提问: {input}"),
        ])

        # 聊天模型
        self.chat_model = ChatTongyi(model=config.chat_model)

        # 最终的执行链
        self.chain = self.__get_chain()

    def document_format(self, docs):
        """
        将检索到的文档列表格式化成字符串，方便放入提示词

        Args:
            docs (list[Document]): _description_

        Returns:
            str: 格式化后的字符串
        """
        return "\n\n".join([doc.page_content for doc in docs])
    
    def print_prompt(self, prompt):
        """
        打印提示词，方便调试

        Args:
            prompt (_type_): _description_

        Returns:
            _type_: _description_
        """
        print("\n--- prompt start ---")
        print(prompt.to_string())
        print("--- prompt end ---\n")
        return prompt
        
    def __get_chain(self):
        """
        获取最终的执行链

        Returns:
            _type_: _description_
        """
        # 获取向量检索器 list[Document]
        retriever = self.vector_service.get_retriever()

        chain = {
            "input": RunnablePassthrough(),
            "context": retriever | self.document_format,
        } | self.prompt_template | self.print_prompt | self.chat_model | StrOutputParser()

        return chain


if __name__ == '__main__':
    rag_service = RagService()
    # res = rag_service.chain.invoke("冬天穿什么颜色衣服比较好看呢？")
    res = rag_service.chain.invoke("我身高 172 cm，体重 120 斤，买衣服应该选什么尺码呢")
    print(res)
