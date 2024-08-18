"""
Evaluation router endpoints
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from backend.database import get_session
from backend.schema.evaluation import EvaluationCreate, EvaluationRead, Evaluation
from typing import List

router = APIRouter()


@router.post("/evaluation", response_model=EvaluationRead)
def create_evaluation(
    request: EvaluationCreate, session: Session = Depends(get_session)
):
    """
    Create a new evaluation record
    """
    new_evaluation = Evaluation(**request.model_dump())
    session.add(new_evaluation)
    session.commit()
    session.refresh(new_evaluation)
    return new_evaluation


@router.get("/evaluations", response_model=List[EvaluationRead])
def read_evaluations(session: Session = Depends(get_session)):
    """
    Read all evaluations
    """
    evaluations = session.execute(select(Evaluation)).all()
    evaluations = [e[0].model_dump() for e in evaluations]
    return evaluations
