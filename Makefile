token_file := .token
token := $(shell cat ${token_file})
version := $(shell cat Version)

run:
	TOKEN=$(token) python3 main.py

test:
	PYTHONPATH=. pytest ./tests/ -vs

print_valutes:
	PYTHONPATH=. python3 ./cmd/valutes.py

build:
	docker build . -t sysdeep_bot:$(version) 
