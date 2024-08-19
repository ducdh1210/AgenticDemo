import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.router.chat import router as chat_router
from backend.router.evaluation import router as evaluation_router

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(evaluation_router)
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Include the evaluation router
# @app.post("/chat")
# async def generate_email(request: InputRquest):
#     user_input = request.user_input

#     if not user_input:
#         raise HTTPException(status_code=400, detail="Human input is required")

#     input_messages = {"messages": [HumanMessage(content=user_input)]}

#     async def event_stream():
#         stream_config = {}  # Add any specific configuration if needed
#         agent_name = ""

#         async for event in runnable.astream_events(
#             input=input_messages,
#             version="v1",
#             config=stream_config,
#         ):
#             # print("Event received:", event)  # Log the raw event
#             kind = event["event"]

#             if kind == "on_tool_end":
#                 if event["name"] == "get_kb_docs":
#                     retrieved_docs = event["data"]["output"]
#                     response = [
#                         {"source": doc.metadata["source"], "chunk": doc.page_content}
#                         for doc in retrieved_docs
#                     ]
#                     yield f"data: {json.dumps({'type': 'on_tool_end', 'output': response})}\n\n"

#             if kind == "on_chain_end":
#                 if event["name"] == "LangGraph":
#                     if event["data"]["output"]["agent"]["messages"]:
#                         output = event["data"]["output"]["agent"]["messages"][0].content
#                         print(">>>> AI answer:", output)
#                         yield f"data: {json.dumps({'type': 'on_chain_end', 'output': output})}\n\n"

#             if kind == "on_chat_model_stream":
#                 content = event["data"]["chunk"].content
#                 if content:
#                     yield f"data: {json.dumps({'type': 'stream', 'content': content, 'agent': agent_name})}\n\n"

#         print("Stream ended")
#         yield "data: [DONE]\n\n"

#     return StreamingResponse(event_stream(), media_type="text/event-stream")
