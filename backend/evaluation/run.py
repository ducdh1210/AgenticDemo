# Evaluation run utilities
import os
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI


def evaluate_length(run: Run, example: Example) -> dict:
    prediction = run.outputs.get("output") or ""
    required = example.outputs.get("answer") or ""
    score = int(len(prediction) < 2 * len(required))
    return {"key": "length", "score": score}


# Initialize Langsmith client
client = Client()

# Retrieve evaluator
evaluators = [
    LangChainStringEvaluator(
        "cot_qa",
        config={
            "llm": ChatOpenAI(model="gpt-4o-mini"),
        },
    ),
    evaluate_length,
]

dataset_name = "qa_eval_clari"


def get_model():
    return None


def answer_qa_question_oai(inputs: dict) -> dict:
    return {"answerrr": "Dummmmy answer"}


# Evaluate the answers for the questions
experiment_results = evaluate(
    answer_qa_question_oai,
    data=dataset_name,
    evaluators=evaluators,
    experiment_prefix="test-qa-eval-clari",
    metadata={
        "variant": "evaluate QA pairs for Clari model",
    },
)

experiment_results
