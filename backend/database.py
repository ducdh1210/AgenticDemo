"""
This module contains the database connection and utility functions like ingestion.
"""

from sqlmodel import create_engine, Session, select
from sqlalchemy.orm import sessionmaker

# Replace this with your actual database URL
from backend.config import CONNECTION_STRING
from backend.schema.document import Document  # Import the Document model

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Function to load documents into the database
def load_documents(
    session: Session, docs_list: list[Document], delete_existing: bool = False
):
    """
    Ingests a list of documents into the database.

    Args:
        session (Session): The database session.
        docs_list (list[Document]): The list of documents to ingest.
        delete_existing (bool, optional): If True, existing documents will be deleted before ingesting new ones. Defaults to False.
    """
    print(f"Ingesting {len(docs_list)} documents to database")

    # Delete existing documents
    if delete_existing:
        stmt = select(Document)
        results = session.exec(stmt).all()
        print(f"Deleting {len(results)} existing documents")
        for result in results:
            session.delete(result)
        session.commit()

    # Ingest new documents
    with session as session:
        for doc in docs_list:
            document = Document(
                source=doc.metadata.get("source", None),
                title=doc.metadata.get("title", None),
                description=doc.metadata.get("description", None),
                language=doc.metadata.get("language", None),
                page_content=doc.page_content,
            )
            session.add(document)
        session.commit()
