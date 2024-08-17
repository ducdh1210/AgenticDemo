from sqlmodel import SQLModel, Field, select, create_engine, Session, Relationship
from sqlalchemy import JSON, Column
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class LangchainPGEmbedding(SQLModel, table=True):
    __tablename__ = "langchain_pg_embedding"

    id: str = Field(primary_key=True, nullable=False)
    collection_id: Optional[UUID] = Field(
        default=None, foreign_key="langchain_pg_collection.uuid"
    )
    embedding: Optional[Any] = Field(default=None, sa_column=Column("embedding"))
    document: Optional[str] = Field(default=None)
    cmetadata: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )

    # Relationships
    collection: Optional["LangchainPGCollection"] = Relationship(
        back_populates="embeddings"
    )


# Additional model for the related `LangchainPGCollection` table (if needed):
class LangchainPGCollection(SQLModel, table=True):
    __tablename__ = "langchain_pg_collection"

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    cmetadata: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )

    embeddings: list["LangchainPGEmbedding"] = Relationship(back_populates="collection")


if __name__ == "__main__":
    from backend.config import CONNECTION_STRING

    # Database connection
    engine = create_engine(CONNECTION_STRING)

    with Session(engine) as session:
        collections = session.exec(select(LangchainPGCollection)).all()
        for collection in collections[:2]:
            print(collection)

    with Session(engine) as session:
        embeddings = session.exec(select(LangchainPGEmbedding)).all()
        for embeddings in embeddings[:2]:
            print(embeddings)
