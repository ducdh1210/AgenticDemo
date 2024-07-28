import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from backend.agents import runnable

# load_dotenv()
print(os.environ["OPENAI_API_KEY"])

if __name__ == "__main__":
    message = "What is button good for?"
    # inputs = {"messages": [HumanMessage(content=message)]}
    # for output in runnable.stream(inputs):
    #     # stream() yields dictionaries with output keyed by node name
    #     for key, value in output.items():
    #         print(f"Output from node '{key}':")
    #         print("---")
    #         print(value)
    #     print("\n---\n")
