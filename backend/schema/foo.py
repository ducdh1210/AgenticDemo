from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from typing import Any, Optional


class Foo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    embedding: Any = Field(sa_column=Column(Vector(3)))
