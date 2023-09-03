-include .env
SOURCE_DIR = src
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_VERSION ?= v$(shell poetry version -s)
PROJECT_NAME ?= my_project
PYTHON_VERSION ?= 3.11
.DEFAULT_GOAL := all

init-env:
	touch .env
	@echo "PROJECT_NAME=${PROJECT_NAME}" >> .env
	@echo "PYTHON_VERSION=${PYTHON_VERSION}" >> .env

init:
	init-env
	poetry install

-check-toml:
	poetry check

-reformat-src:
	poetry run black $(PROJECT_DIRS)
	poetry run isort $(PROJECT_DIRS)

-lint-src:
	poetry run ruff check $(SOURCE_DIR)
	poetry run mypy --install-types --show-error-codes --non-interactive $(SOURCE_DIR)

format: -check-toml -reformat-src

lint: -lint-src

audit:
	poetry run bandit -r $(SOURCE_DIR) -x $(TEST_DIR)

test:
	poetry run pytest $(TEST_DIR)

all: format lint audit test

info:
	@echo "Project name: ${PROJECT_NAME}"
	@echo "Project version: ${PROJECT_VERSION}"
	@echo "Python version: ${PYTHON_VERSION}"
