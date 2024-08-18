# Create a new database

[ ] Create a new database

# Run migrations

If it is the first time you run the migrations, you may need to create a new database first. Here, assume we already have a postgres database (with pgvector support) created, and also assume there are also some tables with embeddings.

Thus, first, we need to create a new migrations folder with `alembic init <folder_name>`. Here we call it `migrations`.

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
