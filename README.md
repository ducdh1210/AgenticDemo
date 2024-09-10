# Introduction

# Backend for AI Agent Proof of Concept

This project showcases the core components of an AI agent system. The backend is designed to answer user questions, identify entities in PDF files, and build a knowledge base by collecting data from the internet and generating knowledge embeddings from scraped web pages.

## Technology Stack

- **Web Framework**: FastAPI
- **Database**: PostgreSQL with pgvector extension
  - Stores embeddings and metadata
- **AI/ML Components**:
  - OpenAI API for Language Model
  - Langchain/Langgraph for application orchestration
  - Langsmith for LLM tracing and evaluation

This backend demonstrates how these technologies can be integrated to create a functional AI agent system.

# Setup (local development)

#### Install Dependencies

Install `poetry` first ([doc](https://python-poetry.org/docs/))

Run the following command to install the necessary dependencies using Poetry

```bash
make setup
```

#### Run Migrations

See [run migrations](#run-migrations)

#### Ingest Data

IMPORTANT: create a new folder `data/train` and specify the the knowledge sources, which are web urls, in `data/train/source.py`.

```bash
data
├── train
│   ├── source.py
```

```
# python `source.py`
urls = [
    "https://ABC.com/",
    "https://XYZ.com/",
]
```

Run the ingestion process, including scraping the webs, chunking the scrapted text, creating embeddings for the chunks and storing them in the database.

```bash
make ingest
```

Check the database to see if the data is ingested correctly.

#### Start the Server

Finally, to start your application server, use:

```bash
make server
```

The server will run on `http://localhost:8000`.

#### Interact with the API

Make sure you have your `.env` file set up with the correct environment variables. See `.env.example`. It requires `OPENAI_API_KEY`, with optional `LANGCHAIN_API_KEY` if you want to use Langsmith.

Make HTTP requests to the API endpoint `/chat` using `curl` or any other HTTP client. Here is an example of how to get the recommendations for a user:

```bash
curl -X 'GET' \
  'http://localhost:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_input": "<question here>"
}'
```

Examples of questions for user input:

```
"tell me about XYZ?"
"extract entities of the PDFs in folder /data/live/?"
```

# Setup (docker) -- TODO

# Run migrations

If it is the first time you run the migrations, you need to create a new database first. Here, assume we already have a postgres database (with pgvector support) created, and also assume there are also some tables with embeddings.

If not, please refer to [postgres installation guide](https://www.postgresql.org/download/) and [pgvector installation guide](https://github.com/pgvector/pgvector)

[ ] TODO: Add README for how to create a new database with pgvector

First we need to create a new migrations folder with `alembic init <folder_name>`. Here we call it `migrations`.

```
alembic init migrations
```

Navigate to the migrations folder, under `migrations/.env`, update the `target_metadata` to point to your database. You may need to import `SQLModel` from `sqlmodel` first.

```
target_metadata = SQLModel.metadata
```

In `run_migrations_online`, replace the engine creation part with our connection string.

```
def run_migrations_online() -> None:
    from backend.config import CONNECTION_STRING
    from sqlalchemy import create_engine

    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(CONNECTION_STRING)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
```

Add this following line in `migrations/script.py.mako`

```
import sqlmodel
```

Now, create a new migration script

```
alembic revision --autogenerate -m "<message>"
```

This will create a new migration script in `migrations/versions`.

Apply migration to the database

```
alembic upgrade head
```
