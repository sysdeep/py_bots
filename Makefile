token_file := .token
token := $(shell cat ${token_file})

run:
	TOKEN=$(token) python3 main.py

test:
	PYTHONPATH=. pytest ./tests/ -vs

print_valutes:
	PYTHONPATH=. python3 ./cmd/valutes.py
