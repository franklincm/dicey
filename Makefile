install-dev: Pipfile
	pre-commit install
	git config --bool flake8.strict true
	pipenv install --dev

test: tests/
	python -m pytest -s

build: setup.py
	python setup.py sdist bdist_wheel

publish: build
	python -m twine upload dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf dicey.egg-info/
