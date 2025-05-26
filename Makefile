# Makefile for grok-lab project
# Simple commands to run tests, examples, and common tasks

.PHONY: help test example clean install lint all

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make test     - Run all tests"
	@echo "  make example  - Run example usage"
	@echo "  make all      - Run tests and example"
	@echo "  make clean    - Clean up __pycache__ and .pyc files"
	@echo "  make install  - Install package in development mode"
	@echo "  make lint     - Run basic code checks (if tools available)"

# Run tests
test:
	@echo "Running tests..."
	python -m unittest grok_api_test.py -v

# Run example
example:
	@echo "Running example (will try to connect to API)..."
	cd examples && python example_usage.py

# Run both tests and example
all: test example

# Clean up Python cache files
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete"

# Install package in development mode
install:
	@echo "Installing package in development mode..."
	pip install -e .

# Basic linting (if flake8 is available)
lint:
	@echo "Running basic code checks..."
	@python -c "import ast; ast.parse(open('grok_api.py').read()); print('✓ grok_api.py syntax OK')" || echo "✗ grok_api.py has syntax errors"
	@python -c "import ast; ast.parse(open('grok_api_test.py').read()); print('✓ grok_api_test.py syntax OK')" || echo "✗ grok_api_test.py has syntax errors"
	@python -c "import ast; ast.parse(open('examples/example_usage.py').read()); print('✓ example_usage.py syntax OK')" || echo "✗ example_usage.py has syntax errors"
