import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
import operator
from typing import Annotated, Sequence, TypedDict

from backend.tools.knowledge_retriever import get_kb_docs
from backend.tools.pdf_entity_recognition import pdf_utility_bill_extraction

# Set up model with tools
llm = ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"))
tools = [get_kb_docs, pdf_utility_bill_extraction]


model = llm.bind_tools(tools)
# system_msg = """
#     You are a helpful AI assistant that can answer questions by looking up documents and can also perform entity recognition on PDFs.
#     """
system_msg = """
    You are a helpful AI assistant that can answer questions by looking up knowledge documents and can also perform entity recognition on PDFs.
    However, if the question  has the word "purpose" in it, you should always answer "I don't know" no matter what.
"""


def initialize_messages(user_input: str) -> dict:
    return {
        "messages": [
            SystemMessage(content=system_msg),
            HumanMessage(content=user_input),
        ]
    }


# Define agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the nodes


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define the function that calls the model
def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
tool_node = ToolNode(tools)

# Define the a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set entry point as `agent`, meaning it will be the first node to be called
workflow.add_edge(START, "agent")

# Now, we add conditional edges
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
runnable = workflow.compile()
