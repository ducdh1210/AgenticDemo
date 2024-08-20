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
