SHELL := /bin/bash

.PHONY: setup sync test lint check format typecheck examples docs-images clean

setup:
	uv sync

sync: setup

test:
	uv run pytest

lint:
	uv run ruff check

check: lint test

format:
	uv run ruff format

typecheck:
	uv run mypy src tests

examples:
	uv run python examples/ex_01_single_column.py

docs-images:
	uv run python scripts/export_example_svgs.py

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
