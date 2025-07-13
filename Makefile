SHELL := /bin/bash
CURDIR := $(shell pwd)


test:
	# -s is to allow dropping into an ipdb debugger
	poetry run pytest -s

test-coverage:
	# poetry run pytest --cov=tna-fcl-client --cov-report=term-missing tests/
	poetry run pytest --cov=tna-fcl-client --cov-report=term-missing

check-types:
	poetry run mypy .

check-syntax:
	poetry run ruff check .

check-format:
	poetry run ruff format .

check-all: check-types check-syntax check-format

testme:
	echo $(HEREGOPATH)

