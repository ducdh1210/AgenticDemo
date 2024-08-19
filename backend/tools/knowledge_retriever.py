import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.tools import tool

from backend.config import CONNECTION_STRING

########################
#    Retriever tool    #
########################
vector_store = PGVector(
    embeddings=OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL")),
    connection=CONNECTION_STRING,
    collection_name=os.getenv("POSTGRESQL_PGVECTOR_COLLECTION"),
)
retriever = vector_store.as_retriever(
    search_type=os.getenv("RETRIEVER_SEARCH_TYPE"),
    search_kwargs={"k": os.getenv("RETRIEVER_NUM_RESULTS")},
)


@tool
def get_kb_docs(query: str) -> list:
    """Returns knowledge base documents most similar to the search query"""
    return retriever.invoke(query)
