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