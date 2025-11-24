#!/bin/bash
# Unix shell script to install dependencies and run the RAG system

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Initializing RAG system with sample data..."
python init_rag.py

echo ""
echo "Starting RAG API server..."
cd src/rag_system
python api/main.py