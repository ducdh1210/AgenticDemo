# Base class for common attributes
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class EvaluationBase(BaseModel):
    question: str
    answer: str
    source: str


# SQLModel for database operations
class Evaluation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: str
    source: str


# Pydantic model for input (request) - Creating a new evaluation
class EvaluationCreate(EvaluationBase):
    pass


# Pydantic model for output (response) - Returning an evaluation
class EvaluationRead(EvaluationBase):
    id: int


# Pydantic model for input (request) - Updating an evaluation
class EvaluationUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    source: Optional[str] = None


# Pydantic model for query parameters
class EvaluationQuery(BaseModel):
    question: Optional[str] = None


# Pydantic model for paginated response
class PaginatedEvaluationResponse(BaseModel):
    total: int
    evaluations: List[EvaluationRead]


if __name__ == "__main__":
    # Database connection
    from backend.config import CONNECTION_STRING
    from sqlmodel import create_engine, Session
    from backend.schema.evaluation import EvaluationCreate

    engine = create_engine(CONNECTION_STRING)

    # Add a new evaluation
    evaluation = EvaluationCreate(
        question="What is the capital of the moon?",
        answer="The moon is not a planet",
        source="NASA",
    )
    with Session(engine) as session:
        session.add(evaluation)
        session.commit()
