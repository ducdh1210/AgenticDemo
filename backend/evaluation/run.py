# Evaluation run utilities
import os
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI

# Initialize Langsmith client
client = Client()


# a dummy evaluator criteria for illustrative purpose
def evaluate_length(run: Run, example: Example) -> dict:
    prediction = run.outputs.get("output") or ""
    required = example.outputs.get("answer") or ""
    score = int(len(prediction) < 2 * len(required))
    return {"key": "length", "score": score}


# Retrieve evaluator
evaluators = [
    LangChainStringEvaluator(
        "cot_qa",
        config={
            "llm": ChatOpenAI(model="gpt-4o-mini"),
        },
    ),
    # evaluate_length,
]

DATASET_NAME = "qa_eval_clari"


def get_copilot_response(inputs: dict) -> dict:
    """Retrieve the copilot agent, feed it ground-truth question,
    and get the response from it"""
    from backend.agents import runnable
    from langchain_core.messages import HumanMessage

    question = inputs.get("question")

    input_messages = {"messages": [HumanMessage(content=question)]}
    result = runnable.invoke(input=input_messages)
    if result["messages"][-1].content:
        response = result["messages"][-1].content
    else:
        response = "No response"
    return {"answer": response}


# Evaluate the answers for the questions
experiment_results = evaluate(
    get_copilot_response,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="test-qa-eval-clari",
    metadata={
        "variant": "evaluate QA pairs for Clari model",
    },
)

experiment_results
