# Define PHONY targets to ensure they are not treated as actual files
.PHONY: lint test

# Target for linting using Black and Flake8
lint:
	@pipenv run black .
	@pipenv run flake8

# Target for running tests using Pytest
test:
	@pipenv run pytest
