# Makefile for Python project

# Tests
.PHONY: tests
tests:
	PYTHONPATH=. pytest tests	

# Linting
.PHONY: ruff
ruff:
	ruff check --fix

# Docs
.PHONY: docs
docs:
	pydocstyle 	

# Docker build
.PHONY: build
build:
	docker build -t ask-qa .

# Docker run
.PHONY: run
run:
	docker run -p 8501:8501 ask-qa