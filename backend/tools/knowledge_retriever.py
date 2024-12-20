import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_pinecone import PineconeVectorStore
from langchain.tools import tool

from backend.config import CONNECTION_STRING
from dotenv import load_dotenv

load_dotenv()

########################
#    Retriever tool    #
########################
# vector_store = PGVector(
#     embeddings=OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL")),
#     connection=CONNECTION_STRING,
#     collection_name=os.getenv("POSTGRESQL_PGVECTOR_COLLECTION"),
# )

# from pinecone import Pinecone, ServerlessSpec

# pinecone_api_key = os.environ.get("PINECONE_API_KEY")
# pc = Pinecone(api_key=pinecone_api_key)
# index_name = os.getenv("PINECONE_INDEX_NAME")

vector_store = PineconeVectorStore(
    # index=pc.Index(index_name),
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL")),
)


# retriever = vector_store.as_retriever(
#     # search_type=os.getenv("RETRIEVER_SEARCH_TYPE"),
#     search_kwargs={"k": os.getenv("RETRIEVER_NUM_RESULTS", 5)},
# )
# print(retriever.invoke("What are some conclusions about anticoagulation"))

retriever = vector_store.as_retriever(
    # search_type=os.getenv("RETRIEVER_SEARCH_TYPE"),
    search_kwargs={"k": 10},
)


@tool
def get_kb_docs(query: str) -> list:
    """Returns knowledge base documents most similar to the search query"""
    response = retriever.invoke(query)
    # Extract source and page content from the response
    response = [
        {"source": doc.metadata["source"], "chunk": doc.page_content}
        for doc in response
    ]

    return response
