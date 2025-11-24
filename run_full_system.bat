@echo off
REM Batch file to run the complete RAG system with React frontend

echo ========================================
echo RAG System - Full Setup
echo ========================================

echo.
echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Installing frontend dependencies...
cd src\rag_system\frontend
npm install

echo.
echo Step 3: Starting the RAG API server...
cd ..\api
start "RAG API Server" /MIN python main.py

echo.
echo Step 4: Starting the React frontend...
cd ..\frontend
start "React Frontend" /MIN npm run start

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The RAG API server is running on http://localhost:8000
echo The React frontend is running on http://localhost:3000
echo.
echo You can now access the chat interface at http://localhost:3000
echo.
echo Press any key to exit...
pause >nul