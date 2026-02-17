.PHONY: fmt lint test test-all test-unit test-integration typecheck ci

fmt:
	uv run ruff format .
	uv run ruff check . --fix

lint:
	uv run ruff check .
	uv run ruff format --check .

test:
	test: test-unit

test-all:
	uv run pytest

test-unit:
	uv run pytest -m "not integration"

test-integration:
	uv run pytest -m integration

typecheck:
	uv run mypy src

ci: lint test-unit
