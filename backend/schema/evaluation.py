# Base class for common attributes
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class EvaluationBase(SQLModel):
    question: str
    answer: str
    source: str


# SQLModel for database operations
class Evaluation(EvaluationBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


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


# note: this is NOT working yet, api is working though
if __name__ == "__main__":
    # Database connection
    from backend.config import CONNECTION_STRING
    from sqlmodel import create_engine, Session, select
    from backend.schema.evaluation import EvaluationCreate

    engine = create_engine(CONNECTION_STRING)
    session = Session(engine)

    # Fetch all evaluations
    evaluations = session.exec(
        select(Evaluation)
    ).all()  # Fetch all instances of Evaluation
    for evaluation in evaluations:
        print(evaluation)  # Print each evaluation instance

    # # Add a new evaluation
    # evaluation = EvaluationCreate(
    #     question="What is the capital of the moon?",
    #     answer="The moon is not a planet",
    #     source="NASA",
    # )
    # evaluation = Evaluation(**evaluation.model_dump())
    # session.add(evaluation)
    # session.commit()
    # session.refresh(evaluation)
