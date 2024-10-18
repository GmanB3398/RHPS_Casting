.PHONY: lint
lint: 
    @pipenv run black .
    @pipenv run flake8

.PHONY: test
test:
    @pipenv run pytest