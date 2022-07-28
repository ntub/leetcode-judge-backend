SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

COMMA := ,

PROJECT_NAME := $(shell echo $(notdir $(CURDIR)) | sed -e 's/_/-/g')
PYTHON_IMAGE_VERSION := $(shell cat .python-version)

CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD  | sed -e 's/_/-/g; s/\//-/g')
CURRENT_VERSION := $(shell git rev-parse --short HEAD)

install: poetry install
.PHONY: install

venv: poetry shell
.PHONY: venv

test:  ## Run check and test
	python src/manage.py check
	python src/manage.py makemigrations --check --dry-run --noinput
	# pytest -s src  # TODO
.PHONY: test

lint:  ## Check lint
	flake8 .
	pydocstyle .
	isort --check --diff .
	black --check --diff .
.PHONY: lint

lint-fix: ## Fix lint
	isort .
	black .
.PHONY: lint-fix

typecheck:  ## Run typechecking
	mypy --show-error-codes --pretty .
.PHONY: typecheck

ci: lint typecheck test  ## Run all checks (lint, typecheck, test)
.PHONY: ci

clean:  ## Clean cache files
	find . -name '__pycache__' -type d | xargs rm -rvf
	find . -name '.mypy_cache' -type d | xargs rm -rvf
	find . -name '.pytest_cache' -type d | xargs rm -rvf
.PHONY: clean

build: Dockerfile  ## Build docker image
	docker build \
		-f $^ \
		--build-arg PYTHON_IMAGE_VERSION=$(PYTHON_IMAGE_VERSION) \
		--tag $(PROJECT_NAME):$(CURRENT_BRANCH) \
		--tag $(PROJECT_NAME):$(CURRENT_VERSION) .
.PHONY: build

run:  ## Run dev server
	python src/manage.py runserver_plus
.PHONY: run

shell:  ## Run shell
	python src/manage.py shell_plus
.PHONY: shell

.DEFAULT_GOAL := help
help: Makefile
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
