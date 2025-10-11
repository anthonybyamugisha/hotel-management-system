# Makefile for Hotel Management System

# Default target
.PHONY: help
help:
	@echo "Hotel Management System - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make setup     - Set up the project (install dependencies, run migrations)"
	@echo "  make run       - Run the development server"
	@echo "  make migrate   - Run database migrations"
	@echo "  make install   - Install dependencies"
	@echo "  make clean     - Remove Python cache files"

# Set up the project
.PHONY: setup
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && python manage.py migrate

# Run the development server
.PHONY: run
run:
	. venv/bin/activate && python manage.py runserver

# Run database migrations
.PHONY: migrate
migrate:
	. venv/bin/activate && python manage.py migrate

# Install dependencies
.PHONY: install
install:
	. venv/bin/activate && pip install -r requirements.txt

# Clean Python cache files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/

# Install dependencies in virtual environment
venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip