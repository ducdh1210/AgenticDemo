import os
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from backend.config import CONNECTION_STRING
from typing import List, Optional

### Tables existed even before the first migration ####


### New tables ###
# class LangchainPGCollection(SQLModel, table=True):
#     uuid: str = Field(default=None, primary_key=True)  # Assuming uuid is a string
#     name: str
#     cmetadata: Optional[dict] = Field(
#         default=None
#     )  # Assuming cmetadata is a JSON field


class Evaluation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question: str
    answer: str
    source: str


# if __name__ == "__main__":
#     # Database connection
#     engine = create_engine(CONNECTION_STRING)

#     # Create tables (only if they don't exist)
#     # TODO: use alembic
#     SQLModel.metadata.create_all(engine)
