# Makefile for grok-lab project
# Simple commands to run tests, examples, and common tasks

.PHONY: help test example clean install lint all scripts digest-performance digest-py digest-js digest-sh digest-optimized

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make test              - Run all tests"
	@echo "  make example           - Run example usage"
	@echo "  make scripts           - Run example shell scripts"
	@echo "  make digest-performance - Compare performance of all digest implementations"
	@echo "  make digest-py         - Run Python digest (original)"
	@echo "  make digest-optimized  - Run optimized Python digest"
	@echo "  make digest-js         - Run JavaScript digest"
	@echo "  make digest-sh         - Run shell script digest"
	@echo "  make all               - Run tests and examples"
	@echo "  make clean             - Clean up __pycache__ and .pyc files"
	@echo "  make install           - Install package in development mode"
	@echo "  make lint              - Run basic code checks (if tools available)"

# Run tests
test:
	@echo "Running tests..."
	python -m unittest grok_api_test.py -v

# Run example
example:
	@echo "Running example (will try to connect to API)..."
	cd examples && python example_usage.py

# Run shell script examples
scripts:
	@echo "Running shell script examples..."
	@echo "Testing API key info..."
	bash examples/api-key-info.sh | head -c 200 && echo ""
	@echo "Testing chat completion..."
	bash examples/chat.sh | head -c 200 && echo ""
	@echo "Testing hello-waw..."
	bash examples/hello-waw.sh | head -c 200 && echo ""
	@echo "Testing digest script..."
	python examples/digest.py | head -c 200 && echo ""

# Performance comparison of digest implementations
digest-performance:
	@echo "=== Performance Comparison: News Digest Implementations ==="
	@echo ""
	@echo "1. Shell Script (curl + bash):"
	@time bash examples/digest.sh > /dev/null 2>&1 || echo "Shell script failed"
	@echo ""
	@echo "2. JavaScript (Node.js native HTTPS):"
	@time node examples/digest.js > /dev/null 2>&1 || echo "JavaScript script failed"
	@echo ""
	@echo "3. Python Original (requests):"
	@time python examples/digest.py > /dev/null 2>&1 || echo "Python original script failed"
	@echo ""
	@echo "4. Python Optimized (requests with connection pooling):"
	@time python examples/digest_optimized.py > /dev/null 2>&1 || echo "Python optimized script failed"
	@echo ""
	@echo "=== Performance comparison complete ==="

# Individual digest implementations
digest-py:
	@echo "Running Python digest (original)..."
	python examples/digest.py

digest-optimized:
	@echo "Running Python digest (optimized)..."
	python examples/digest_optimized.py

digest-js:
	@echo "Running JavaScript digest..."
	node examples/digest.js

digest-sh:
	@echo "Running shell script digest..."
	bash examples/digest.sh

# Run both tests and examples
all: test example scripts

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
