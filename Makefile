token_file := .token
token := $(shell cat ${token_file})

run:
	TOKEN=$(token) python3 main.py
