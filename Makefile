.PHONY: ingest main server

run-python-module = poetry run python -m backend.$(1)

ingest:
	$(call run-python-module,ingest)

main: 
	$(call run-python-module,main)

server: 
	$(call run-python-module,server)