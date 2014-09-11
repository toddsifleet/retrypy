.PHONY: test
test: clean lint
	@py.test -s test

.PHONY: lint
lint:
	@flake8 retry test

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -exec rm {} ';'

.PHONY: bootstrap
bootstrap:
	@pip install -r requirements-dev.txt
	@pip install -e .
