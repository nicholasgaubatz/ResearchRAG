.PHONY: fmt lint test typecheck

fmt:
	ruff format .
	ruff check . --fix

lint:
	ruff check .
	ruff format --check .

test:
	pytest

typecheck:
	mypy src
