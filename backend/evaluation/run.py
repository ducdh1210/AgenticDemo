# Evaluation run utilities
import os
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator


# Initialize Langsmith client
client = Client()

# Retrieve evaluator
qa_evaluator = [LangChainStringEvaluator("cot_qa")]

dataset_name = "qa_eval_clari"


def get_model():
    return None


def answer_qa_question_oai(inputs: dict) -> dict:
    return {"answer": "Dummy answer"}


# Evaluate the answers for the questions
experiment_results = evaluate(
    answer_qa_question_oai,
    data=dataset_name,
    evaluators=qa_evaluator,
    experiment_prefix="test-qa-eval-clari",
    metadata={
        "variant": "evaluate QA pairs for Clari model",
    },
)
