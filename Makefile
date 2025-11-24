# Makefile for RAG System

# Variables
PYTHON := python
PIP := pip
SRC_DIR := src
DATA_DIR := data
INDEXES_DIR := indexes

# Default target
.PHONY: help
help:
	@echo "RAG System Makefile"
	@echo "=================="
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  init        - Initialize with sample data"
	@echo "  test        - Run tests"
	@echo "  evaluate    - Evaluate system performance"
	@echo "  run         - Start the API server"
	@echo "  cli-test    - Run CLI test"
	@echo "  clean       - Clean data and indexes"
	@echo "  docker      - Build and run with Docker"
	@echo "  docker-dev  - Run Docker in development mode"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Initialize with sample data
.PHONY: init
init:
	$(PYTHON) init_rag.py

# Run tests
.PHONY: test
test:
	$(PYTHON) test_rag.py

# Evaluate system performance
.PHONY: evaluate
evaluate:
	$(PYTHON) evaluate_rag.py

# Start the API server
.PHONY: run
run:
	$(PYTHON) $(SRC_DIR)/rag_system/api/main.py

# Run CLI test
.PHONY: cli-test
cli-test:
	$(PYTHON) rag_cli.py test

# Clean data and indexes
.PHONY: clean
clean:
	rm -rf $(DATA_DIR)/*
	rm -rf $(INDEXES_DIR)/*

# Build and run with Docker
.PHONY: docker
docker:
	docker-compose up --build

# Run Docker in development mode
.PHONY: docker-dev
docker-dev:
	docker-compose up

# Run data loader example
.PHONY: load-data
load-data:
	$(PYTHON) load_data.py