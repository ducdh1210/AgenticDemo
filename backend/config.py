from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Set up database connection
USER_NAME = os.getenv("POSTGRESQL_USERNAME")
PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
HOST = os.getenv("POSTGRESQL_HOST")
PORT = os.getenv("POSTGRESQL_PORT")
DATABASE = os.getenv("POSTGRESQL_DATABASE")
COLLECTION_NAME = os.getenv("POSTGRESQL_PGVECTOR_COLLECTION")
CONNECTION_STRING = (
    f"postgresql+psycopg://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# Set up OpenAI variables
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
