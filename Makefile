ALLMODULES=$(patsubst %.py, %.py, $(wildcard tests/test_*.py))

clean: clean-build

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

install:
	pip install -e .

dist: clean
	python setup.py sdist
	ls -l dist

test:
	python -m unittest -v -b $(ALLMODULES)

.PHONY: test