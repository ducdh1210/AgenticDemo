"""
Chat router endpoints
"""

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from backend.agents import runnable, initialize_messages


class InputRquest(BaseModel):
    user_input: str


router = APIRouter()


@router.post("/chat")
async def generate_email(request: InputRquest):
    """
    Generate a response from copilot
    """
    user_input = request.user_input

    if not user_input:
        raise HTTPException(status_code=400, detail="Human input is required")

    input_messages = initialize_messages(user_input)

    async def event_stream():
        stream_config = {}  # Add any specific configuration if needed
        agent_name = ""

        async for event in runnable.astream_events(
            input=input_messages,
            version="v1",
            config=stream_config,
        ):
            # print("Event received:", event)  # Log the raw event
            kind = event["event"]

            if kind == "on_tool_end":
                if event["name"] == "get_kb_docs":
                    # try:
                    #     retrieved_docs = event["data"]["output"]
                    #     response = [
                    #         {
                    #             "source": doc.metadata["source"],
                    #             "chunk": doc.page_content,
                    #         }
                    #         for doc in retrieved_docs
                    #     ]
                    # except Exception as e:
                    response = eval(event["data"]["output"].content)
                    yield f"data: {json.dumps({'type': 'on_tool_end', 'output': response})}\n\n"

            if kind == "on_chain_end":
                if event["name"] == "LangGraph":
                    if event["data"]["output"]["agent"]["messages"]:
                        output = event["data"]["output"]["agent"]["messages"][0].content
                        print(">>>> AI answer:", output)
                        yield f"data: {json.dumps({'type': 'on_chain_end', 'output': output})}\n\n"

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield f"data: {json.dumps({'type': 'stream', 'content': content, 'agent': agent_name})}\n\n"

        print("Stream ended")
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
