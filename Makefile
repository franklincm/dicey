install-dev: pyproject.toml
	poetry install
	pre-commit install
	git config --bool flake8.strict true

test: tests/
	python -m pytest -s

build: setup.py
	python setup.py sdist bdist_wheel

publish: build
	python -m twine upload dist/*

clean:
	$(RM) -r build/
	$(RM) -r dist/
	$(RM) -r dicey.egg-info/
