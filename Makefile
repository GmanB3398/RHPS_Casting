.PHONY: lint
lint: 
	@poetry run black .
	@poetry run ruff check . --fix --unsafe-fixes
	@poetry run mypy -p src --check-untyped-defs

.PHONY: test
test:
	@poetry run python -m pytest -v --full-trace
  