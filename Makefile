.PHONY: ingest evaluate server

run-python-module = poetry run python -m backend.$(1)

ingest:
	$(call run-python-module,ingest)

evaluate: 
	$(call run-python-module,evaluate)

server: 
	$(call run-python-module,server)