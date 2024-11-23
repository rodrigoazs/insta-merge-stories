.PHONY: tests

format:
	poetry run ruff check . --select I --fix
	poetry run ruff format .