# Python version and virtualenv locations
PYTHON ?= python3
VENV_DIR = .venv
VENV_DEV = $(VENV_DIR)/dev
VENV_TEST = $(VENV_DIR)/test
VENV_PROD = $(VENV_DIR)/prod

# Virtual environment binaries
VENV_BIN = bin
ifeq ($(OS),Windows_NT)
    VENV_BIN = Scripts
endif

# Commands with virtual environment paths
DEV_PYTHON = $(VENV_DEV)/$(VENV_BIN)/python
DEV_PIP = $(VENV_DEV)/$(VENV_BIN)/pip
TEST_PYTHON = $(VENV_TEST)/$(VENV_BIN)/python
TEST_PIP = $(VENV_TEST)/$(VENV_BIN)/pip
PROD_PYTHON = $(VENV_PROD)/$(VENV_BIN)/python
PROD_PIP = $(VENV_PROD)/$(VENV_BIN)/pip

.PHONY: help clean install develop test lint format publish-test publish venv-dev venv-test venv-prod

help:
	@echo "Imitatus Makefile commands:"
	@echo "Virtual Environments:"
	@echo "  make venv-dev     - Create development virtual environment"
	@echo "  make venv-test    - Create testing virtual environment"
	@echo "  make venv-prod    - Create production virtual environment"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install package in production environment"
	@echo "  make develop      - Install package and dev tools in development environment"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-api     - Run API tests only"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""
	@echo "Development:"
	@echo "  make lint         - Check style with flake8"
	@echo "  make format       - Format code with black"
	@echo "  make run-dev      - Run server in development mode"
	@echo "  make run-prod     - Run server in production mode"
	@echo ""
	@echo "Distribution:"
	@echo "  make build        - Build package distributions"
	@echo "  make publish-test - Publish to TestPyPI"
	@echo "  make publish      - Publish to PyPI"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make clean-venv   - Remove all virtual environments"

# Virtual environments
venv-dev:
	$(PYTHON) -m venv $(VENV_DEV)
	$(DEV_PIP) install --upgrade pip
	$(DEV_PIP) install -r requirements-dev.txt
	$(DEV_PIP) install -e .

venv-test:
	$(PYTHON) -m venv $(VENV_TEST)
	$(TEST_PIP) install --upgrade pip
	$(TEST_PIP) install -r requirements-test.txt
	$(TEST_PIP) install -e .

venv-prod:
	$(PYTHON) -m venv $(VENV_PROD)
	$(PROD_PIP) install --upgrade pip
	$(PROD_PIP) install -r requirements.txt
	$(PROD_PIP) install .

# Installation
install: venv-prod

develop: venv-dev

# Testing commands
test: venv-test
	$(TEST_PYTHON) -m pytest tests/ -v --cov=src/imitatus

test-unit: venv-test
	$(TEST_PYTHON) -m pytest tests/unit -v --cov=src/imitatus

test-api: venv-test
	$(TEST_PYTHON) -m pytest tests/api -v --cov=src/imitatus

test-coverage: venv-test
	$(TEST_PYTHON) -m pytest tests/ -v --cov=src/imitatus --cov-report=html --cov-report=term

# Development commands
lint: venv-dev
	$(DEV_PYTHON) -m flake8 src/imitatus tests
	$(DEV_PYTHON) -m black --check src/imitatus tests
	$(DEV_PYTHON) -m isort --check-only src/imitatus tests

format: venv-dev
	$(DEV_PYTHON) -m black src/imitatus tests
	$(DEV_PYTHON) -m isort src/imitatus tests

# Build and publish
build: clean venv-dev
	$(DEV_PYTHON) -m build

publish-test: build
	$(DEV_PYTHON) -m twine upload --repository testpypi dist/*

publish: build
	$(DEV_PYTHON) -m twine upload dist/*

# Run servers
run-dev: venv-dev
	$(DEV_PYTHON) -m imitatus.server --debug

run-prod: venv-prod
	$(PROD_PYTHON) -m imitatus.server

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

clean-venv:
	rm -rf $(VENV_DIR)

# Full clean and setup
reset: clean clean-venv venv-dev venv-test venv-prod
