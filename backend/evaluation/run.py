# Evaluation run utilities
import os
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI


# a dummy evaluator criteria for illustrative purpose
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


def get_copilot_response(inputs: dict) -> dict:
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
    data=dataset_name,
    evaluators=evaluators,
    experiment_prefix="test-qa-eval-clari",
    metadata={
        "variant": "evaluate QA pairs for Clari model",
    },
)

experiment_results
