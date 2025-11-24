# RAG System Startup Guide

This guide will help you run the complete RAG system with a React-based chat interface similar to ChatGPT, Gemini, or Grok.

## Prerequisites

Before running the system, ensure you have the following installed:
- Python 3.10+
- Node.js 16+
- npm 8+

## Quick Start Options

### Option 1: Run Everything Locally (Recommended for Development)

1. **Install all dependencies**:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install frontend dependencies
   cd src/rag_system/frontend
   npm install
   ```

2. **Initialize the RAG system with sample data**:
   ```bash
   # Go back to the root directory
   cd ../../..
   python init_rag.py
   ```

3. **Start the backend API server**:
   ```bash
   cd src/rag_system/api
   python main.py
   ```
   The API will be available at `http://localhost:8000`

4. **Start the React frontend**:
   ```bash
   # In a new terminal, from the root directory
   cd src/rag_system/frontend
   npm run start
   ```
   The frontend will be available at `http://localhost:3000`

### Option 2: Use the Automated Scripts

For Windows:
```bash
run_full_system.bat
```

For Unix/Linux/Mac:
```bash
chmod +x run_full_system.sh
./run_full_system.sh
```

### Option 3: Run with Docker (Recommended for Production)

```bash
docker-compose up --build
```

The complete system will be available at `http://localhost:8000`

## Using the Chat Interface

Once the system is running, you can access the chat interface at `http://localhost:3000` (or `http://localhost:8000` if using Docker).

### Features:
- Real-time chat interface with typing indicators
- Source citations for all answers
- Example queries to get started
- Responsive design for desktop and mobile

### Example Questions:
- "Who led the Salt Satyagraha in 1930 and why was it important?"
- "What was the purpose of the Salt March?"
- "When did India gain independence?"

## Project Structure

```
RAG/
├── src/
│   └── rag_system/
│       ├── api/           # FastAPI backend
│       ├── frontend/      # React chat interface
│       ├── data/          # Data processing modules
│       ├── models/        # ML models (embedding, generation)
│       └── rag_pipeline.py # Main RAG pipeline
├── data/                  # Runtime data storage
├── indexes/               # Vector index storage
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile.full        # Full system Dockerfile
└── ...
```

## Customization

### Changing the Domain
To customize the system for a different domain:
1. Add your domain-specific documents using the data loading scripts
2. Rebuild the index with your new documents
3. The system will now answer questions specific to your domain

### Styling
To customize the look and feel:
- Modify `src/rag_system/frontend/src/components/ChatInterface.css`
- Update colors, fonts, and layout in the CSS file

### API Endpoints
The backend provides the following REST API endpoints:
- `POST /query` - Submit a question and receive an answer with sources
- `POST /add_documents` - Add new documents to the knowledge base
- `POST /build_index` - Rebuild the search index after adding documents

## Troubleshooting

### Common Issues:

1. **Port already in use**:
   - Change the port in `config.json` or stop the process using the port

2. **Dependencies not installing**:
   - Ensure you have Python 3.10+ and Node.js 16+ installed
   - Try upgrading pip: `pip install --upgrade pip`

3. **Frontend not connecting to backend**:
   - Check that the API server is running on `http://localhost:8000`
   - Verify the proxy settings in `vite.config.js`

### Need Help?
If you encounter any issues, check the console logs for error messages or refer to the documentation in each component directory.