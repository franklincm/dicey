install-dev: Pipfile
	pre-commit install
	git config --bool flake8.strict true
	pipenv install --dev

test: tests/
	python -m pytest
