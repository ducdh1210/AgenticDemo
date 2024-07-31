from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.tools import tool

from backend.config import COLLECTION_NAME, CONNECTION_STRING, OPENAI_EMBEDDING_MODEL

########################
#    Retriever tool    #
########################
vector_store = PGVector(
    embeddings=OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL),
    connection=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
)
retriever = vector_store.as_retriever()


@tool
def get_kb_docs(query: str) -> list:
    """Returns knowledge base documents most similar to the search query"""
    return retriever.invoke(query)
