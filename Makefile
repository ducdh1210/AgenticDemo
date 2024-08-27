.PHONY: ingest evaluate server create_embeddings seed_data clean setup migrate

run-python-module = poetry run python -m backend.$(1)
run-scripts = poetry run python -m backend.scripts.$(1)

evaluate: 
	$(call run-python-module,evaluate)

server: 
	$(call run-python-module,server)

create_embeddings:
	$(call run-scripts,create_embeddings)

seed_data:
	$(call run-scripts,seed_data)

ingest: create_embeddings seed_data

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

setup:
	poetry install

migrate:
	poetry run alembic upgrade head

# Add this target to run migrations and seed data
init_db: migrate ingest

# Add this target for a full setup
full_setup: setup migrate create_embeddings seed_data