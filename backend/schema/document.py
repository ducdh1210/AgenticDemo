from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# Base class for common attributes of Document
class DocumentBase(SQLModel):
    source: str
    title: str
    description: Optional[str] = None
    language: str
    page_content: str


# SQLModel for database operations
class Document(DocumentBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


# Pydantic model for input (request) - Creating a new document
class DocumentCreate(DocumentBase):
    pass


# Pydantic model for output (response) - Returning a document
class DocumentRead(DocumentBase):
    id: int


# Pydantic model for input (request) - Updating a document
class DocumentUpdate(BaseModel):
    source: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    page_content: Optional[str] = None


# Pydantic model for query parameters
class DocumentQuery(BaseModel):
    title: Optional[str] = None
    language: Optional[str] = None


# Pydantic model for paginated response
class PaginatedDocumentResponse(BaseModel):
    total: int
    documents: List[DocumentRead]
