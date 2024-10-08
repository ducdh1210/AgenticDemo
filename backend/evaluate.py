import os
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langsmith.schemas import Run, Example
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

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
            "llm": ChatOpenAI(model=os.getenv("EVALUATION_MODEL")),
        },
    ),
    # evaluate_length,
]


def get_copilot_response(inputs: dict) -> dict:
    """Gets the copilot agent's response to the ground-truth question.

    Args:
        inputs (dict): A dictionary containing the question to be asked to the copilot agent.

    Returns:
        dict: A dictionary containing the response from the copilot agent.

    """
    from backend.agents import runnable, initialize_messages  # import agent runnable
    from langchain_core.messages import HumanMessage

    input_messages = initialize_messages(user_input=inputs.get("question"))
    result = runnable.invoke(input=input_messages)
    if result["messages"][-1].content:
        response = result["messages"][-1].content
    else:
        response = "No response"
    return {"answer": response}


if __name__ == "__main__":
    # Evaluate the answers for the questions
    experiment_results = evaluate(
        get_copilot_response,
        data=os.getenv("EVALUATION_DATASET_NAME"),
        evaluators=evaluators,
        experiment_prefix=os.getenv("EVALUATION_EXPERIMENT_PREFIX"),
    )
