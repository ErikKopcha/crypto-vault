.PHONY: setup run test clean install

# Default virtual environment path
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Setup virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Run the web application
run:
	$(PYTHON) run.py

# Run CLI encrypt command
encrypt:
	$(PYTHON) cli.py encrypt $(data) $(password)

# Run CLI decrypt command
decrypt:
	$(PYTHON) cli.py decrypt $(file) $(password)

# Run tests
test:
	$(PYTHON) -m pytest

# Clean up generated files
clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf app/utils/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Install the package in development mode
install:
	$(PIP) install -e . 