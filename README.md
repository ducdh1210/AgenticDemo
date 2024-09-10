# Introduction

This is the backend of a POC AI agent project. It handles different types of user requests, such as answering questions or identifying entities in PDF files. It also collects data from the internet, generates knowledge embeddings, and uses a Large Language Model (LLM) for question-answer capabilities. The web app is built using FastAPI and relies on a PostgreSQL database with pgvector for managing and querying embeddings.

# Setup (local development)

### Setup

To set up the project, follow these steps:

#### Install Dependencies

Install `poetry` first ([doc](https://python-poetry.org/docs/))

Run the following command to install the necessary dependencies using Poetry

```bash
make setup
```

#### Run Migrations

See [run migrations](#run-migrations)

#### Create Embeddings

Generate the necessary embeddings for your application

```bash
make create_embeddings
```

#### Ingest Data

IMPORTANT: create a new folder `data/train` and put the data you want to train the model in `data/train/source.py`.

```bash
data
├── train
│   ├── source.py
```

```
# source.py
urls = [
    "https://XYZ.com/",
]
```

```python
urls = [
    "https://XYZ.com/",
]
```

If you want to run the ingestion process that depends on creating embeddings and seeding data, execute:

```bash
make ingest
```

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
