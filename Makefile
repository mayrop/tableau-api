# Makefile for python code
#
# > make help
#
#

INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

.PHONY: help
help:
	@echo 'Current environment: ${ENV}'
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

.PHONY: install
install: ## Sets up local environment and installs requirements
install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) config virtualenvs.in-project true
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: lint
lint: ## Run linter
lint: $(INSTALL_STAMP)
	# stop the build if there are Python syntax errors or undefined names
	$(POETRY) run flake8 --config .flake8 . --count --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	$(POETRY) run flake8 --config .flake8 . --count --exit-zero --statistics
	# run pylint errors
	$(POETRY) run pylint --rcfile pylintrc --recursive=y .
	# Check security issues
	$(POETRY) run bandit -c pyproject.toml -r . -s B608

.PHONY: fix
fix: ## Fix app to Google
fix: $(INSTALL_STAMP)
	black .

.PHONY: dependencies
dependencies: ## Create dependencies files
dependencies: $(INSTALL_STAMP)
	$(POETRY) export --without-hashes -f requirements.txt --output requirements.txt
	$(POETRY) export --without-hashes -f requirements.txt --output requirements-test.txt --with dev

.PHONY: test
test: ## Run tests
test: $(INSTALL_STAMP)
	pytest -v -s

.PHONY: testu
testu: ## Run tests and update snapshot
testu: $(INSTALL_STAMP)
	pytest -v -s --snapshot-update