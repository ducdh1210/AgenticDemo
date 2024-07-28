from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from backend.config import CONNECTION_STRING, COLLECTION_NAME, OPENAI_EMBEDDING_MODEL


# Load and create list of documents
urls = [
    "https://www.usebutton.com/",
    "https://www.usebutton.com/for-publishers",
    "https://www.usebutton.com/for-retailers",
    "https://www.usebutton.com/for-creators",
    "https://www.usebutton.com/button-marketplace",
]
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

print(f"Number of embedding documents: {len(docs_list)}")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)

print(f"Number of text splits: {len(doc_splits)}")

# Specify embedding model
embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

# Add to vectorDB
vector_store = PGVector.from_documents(
    embedding=embedding,
    documents=doc_splits,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
)
