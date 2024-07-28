from langchain_openai import ChatOpenAI
from backend.config import OPENAI_CHAT_MODEL
from langchain_core.messages import HumanMessage
from backend.tools import tools

llm = ChatOpenAI(model=OPENAI_CHAT_MODEL)
model = llm.bind_tools(tools)

inputs = [HumanMessage(content="what is button good for?")]

print(model.invoke(inputs))
