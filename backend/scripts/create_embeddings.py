import os
from typing import Any, Dict, List

from langchain.docstore.document import Document
from langchain.schema import BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langsmith import Client
from sqlmodel import Session, create_engine

from data.train.source import urls
from backend.config import COLLECTION_NAME, CONNECTION_STRING
from backend.database import load_documents
from backend.evaluation.chain import create_structured_qa_chain

# Create database session
engine = create_engine(CONNECTION_STRING)
session = Session(engine)


def scrape_documents(urls: List[str]) -> List[Document]:
    """
    Load documents from given URLs.

    Args:
        urls (List[str]): A list of URLs to load documents from.

    Returns:
        List[Document]: A list of loaded documents.
    """
    docs = [WebBaseLoader(url).load() for url in urls]

    # Flatten the list of lists into a single list
    docs_list = [item for sublist in docs for item in sublist]

    for doc in docs_list:
        # Remove newlines
        doc.page_content = doc.page_content.replace("\n", "")
        # Change tabs to spaces
        doc.page_content = doc.page_content.replace("\t", " ")

    print(f"Number of documents: {len(docs_list)}")

    return docs_list


def split_documents(docs_list: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks.

    Args:
        docs_list (List[Document]): A list of documents to split.

    Returns:
        List[Document]: A list of split document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=200, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)
    print(f"Number of text splits: {len(doc_splits)}")
    return doc_splits


def generate_embeddings(docs_list: List[Document]) -> BaseRetriever:
    """
    Generate embeddings for given documents and store them in a vector database.

    Args:
        docs_list (List[Document]): A list of documents to generate embeddings for.

    Returns:
        BaseRetriever: A vector store containing the generated embeddings.
    """
    # Split documents into smaller chunks
    doc_splits = split_documents(docs_list)

    # Specify embedding model
    embedding = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    # Add to vectorDB
    vector_store = PGVector.from_documents(
        embedding=embedding,
        documents=doc_splits,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,
    )

    return vector_store


def generate_qa_pairs(docs_list: List[Document]) -> List[Dict[str, str]]:
    """
    Generate QA pairs from documents.

    Args:
        docs_list (List[Document]): A list of documents to generate QA pairs from.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing generated QA pairs.
    """
    print(f"Generating QA pairs for {len(docs_list)} documents.")
    qa_chain = create_structured_qa_chain()
    results = qa_chain.batch([doc.page_content for doc in docs_list])
    print(f"Number of QA pairs generated: {len(results)}")
    return results


def store_evaluation_data(results: List[Dict[str, str]]) -> Any:
    """
    Store QA pairs in LangSmith dataset.

    Args:
        results (List[Dict[str, str]]): A list of dictionaries containing QA pairs.

    Returns:
        Any: The created dataset object.
    """
    dataset_name = os.getenv("EVALUATION_DATASET_NAME")
    client = Client()
    datasets = client.list_datasets()
    matching_datasets = [
        dataset for dataset in datasets if dataset.name == dataset_name
    ]
    if len(matching_datasets) == 0:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=os.getenv("EVALUATION_DATASET_DESC"),
        )
    else:
        dataset = matching_datasets[0]

    inputs = [{"question": result.question} for result in results]
    outputs = [{"answer": result.answer} for result in results]

    client.create_examples(
        inputs=inputs,
        outputs=outputs,
        dataset_id=dataset.id,
    )

    return dataset


def generate_evaluation_data(docs_list: List[Document]) -> Any:
    """
    Generate evaluation data from given documents.

    Args:
        docs_list (List[Document]): A list of documents to generate evaluation data from.

    Returns:
        Any: The created dataset object containing the evaluation data.
    """
    qa_pairs = generate_qa_pairs(docs_list)
    dataset = store_evaluation_data(qa_pairs)
    return dataset


def ingest(urls: List[str]) -> None:
    # Scrape documents
    docs_list = scrape_documents(urls)

    # Ingest documents to database
    load_documents(session=session, docs_list=docs_list, delete_existing=True)

    # Compute embeddings associated with new document chunks
    # and update vector store with the computed embeddings
    _ = generate_embeddings(docs_list)

    # Generate evaluation data associated with the new documents
    _ = generate_evaluation_data(docs_list)

    print(f"Ingested {len(docs_list)} documents.")


# Example usage
if __name__ == "__main__":
    ingest(urls)

    # import argparse

    # parser = argparse.ArgumentParser(
    #     description="Ingest documents from a list of URLs."
    # )
    # parser.add_argument(
    #     "urls", metavar="URL", type=str, nargs="+", help="a list of URLs to ingest"
    # )

    # args = parser.parse_args()

    # ingest(args.urls)
