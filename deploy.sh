#!/bin/bash
# Deployment script for the RAG system

echo "========================================"
echo "RAG System - Production Deployment"
echo "========================================"

echo ""
echo "Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Building the React frontend..."
cd src/rag_system/frontend
npm install
npm run build

echo ""
echo "Step 3: Moving built files to serve directory..."
mkdir -p ../../../static
cp -r dist/* ../../../static/

echo ""
echo "Step 4: Starting the production server..."
cd ../../api
python main.py

echo ""
echo "Deployment complete! The RAG system is now running in production mode."