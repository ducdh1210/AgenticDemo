# from langchain_community.document_loaders import TextLoader, WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_postgres.vectorstores import PGVector
# from backend.config import CONNECTION_STRING, COLLECTION_NAME, OPENAI_EMBEDDING_MODEL


# # Load and create list of documents
# urls = [
#     "https://www.clari.com/",
#     "https://www.clari.com/why-clari/",
#     "https://www.clari.com/products/revai/",
#     "https://www.clari.com/solutions/revenue-productivity/",
#     "https://www.clari.com/solutions/revenue-execution/",
#     "https://www.clari.com/solutions/revenue-orchestration/",
#     "https://www.clari.com/revenue-cadence/",
# ]
# docs = [WebBaseLoader(url).load() for url in urls]
# docs_list = [item for sublist in docs for item in sublist]

# ### Generate embeddings

# print(f"Number of embedding documents: {len(docs_list)}")

# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#     chunk_size=200, chunk_overlap=50
# )
# doc_splits = text_splitter.split_documents(docs_list)

# print(f"Number of text splits: {len(doc_splits)}")

# # # Specify embedding model
# # embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

# # # Add to vectorDB
# # vector_store = PGVector.from_documents(
# #     embedding=embedding,
# #     documents=doc_splits,
# #     collection_name=COLLECTION_NAME,
# #     connection=CONNECTION_STRING,
# #     pre_delete_collection=True,
# # )

# # TODO: seperate the Generate embeddings step from the evaluation step
# ### Generate evaluation data
# from backend.evaluation.runnable import create_structured_qa_chain

# qa_chain = create_structured_qa_chain()
# print(f"Number of documents: {len(docs_list)}")
# results = qa_chain.batch([doc.page_content for doc in docs_list[:2]])
# print(f"Number of results: {len(results)}")

# from langsmith import Client

# client = Client()
# dataset_name = "qa_eval_clari"

# # Store the dataset
# dataset = client.create_dataset(
#     dataset_name=dataset_name,
#     description="QA pairs about Clari model.",
# )

# inputs = [{"question": result.question} for result in results]
# outputs = [{"answer": result.answer} for result in results]

# client.create_examples(
#     inputs=inputs,
#     outputs=outputs,
#     dataset_id=dataset.id,
# )

from typing import List, Dict, Any
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.docstore.document import Document
from langchain.schema import BaseRetriever
from backend.config import CONNECTION_STRING, COLLECTION_NAME, OPENAI_EMBEDDING_MODEL
from backend.evaluation.runnable import create_structured_qa_chain
from langsmith import Client


def load_documents(urls: List[str]) -> List[Document]:
    """
    Load documents from given URLs.

    Args:
        urls (List[str]): A list of URLs to load documents from.

    Returns:
        List[Document]: A list of loaded documents.
    """
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
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
    doc_splits = split_documents(docs_list)

    # Specify embedding model
    embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    # Add to vectorDB
    vector_store = PGVector.from_documents(
        embedding=embedding,
        documents=doc_splits,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,
    )

    return vector_store


def generate_qa_pairs(
    docs_list: List[Document], num_docs: int = 2
) -> List[Dict[str, str]]:
    """
    Generate QA pairs from documents.

    Args:
        docs_list (List[Document]): A list of documents to generate QA pairs from.
        num_docs (int, optional): Number of documents to use for QA pair generation. Defaults to 2.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing generated QA pairs.
    """
    qa_chain = create_structured_qa_chain()
    results = qa_chain.batch([doc.page_content for doc in docs_list[:num_docs]])
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
    client = Client()
    dataset_name = "qa_eval_clari"
    datasets = client.list_datasets()
    matching_datasets = [
        dataset for dataset in datasets if dataset.name == dataset_name
    ]
    if len(matching_datasets) == 0:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="QA pairs about Clari model.",
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
    results = generate_qa_pairs(docs_list)
    dataset = store_evaluation_data(results)
    return dataset


# Example usage
if __name__ == "__main__":
    urls = [
        "https://www.clari.com/",
        "https://www.clari.com/why-clari/",
        "https://www.clari.com/products/revai/",
        "https://www.clari.com/solutions/revenue-productivity/",
        "https://www.clari.com/solutions/revenue-execution/",
        "https://www.clari.com/solutions/revenue-orchestration/",
        "https://www.clari.com/revenue-cadence/",
    ]

    # Load documents once
    docs_list = load_documents(urls)

    # Generate embeddings
    # vector_store = generate_embeddings(docs_list)
    # print("Embeddings generated and stored in vector database.")

    # Generate evaluation data
    dataset = generate_evaluation_data(docs_list)
    print("Evaluation data generated and stored.")
