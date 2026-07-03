from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory

from ithiema.RAG项目案例.file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class RAGService(object):

    def __init__(self):
        self.vector_store = VectorStoreService(
            DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt = ChatPromptTemplate.from_template(
            [
                ("system","以我提供的己知参考资料为主,"
                "简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system","并且我提供用户的对话记录，如下："),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问:{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

        def __get_chain(self):
            retrieve = self.vector_store.get_retriever()

            def formart_document(docs:list[Document]):
                if not docs:
                    return "无相关参考资料"

                formart_str = ""
                for doc in docs:
                    formart_str+= f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
                return formart_str

            chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": retrieve | formart_document
                } | self.prompt | self.chat_model | StrOutputParser()
            )

            RunnableWithMessageHistory(
                chain,
                get_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )
            return  chain