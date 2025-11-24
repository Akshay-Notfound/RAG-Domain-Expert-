# Domain-Focused Retrieval-Augmented Generation (RAG) System

A specialized RAG system that operates within a chosen domain to retrieve only domain-relevant evidence and generate precise, source-grounded answers.

## Features

- **Domain-focused**: Specialized for a specific domain (e.g., history, science, literature)
- **Retrieval**: Uses vector similarity search to find relevant documents
- **Generation**: Uses language models to generate accurate answers based on retrieved evidence
- **Source citation**: Provides source information for all answers
- **API**: RESTful API for easy integration
- **Web UI**: Simple web interface for demonstration
- **Containerized**: Docker support for easy deployment
- **Wikipedia Integration**: Fetch and integrate Wikipedia's featured articles
- **Advanced Wikipedia API**: Comprehensive Wikipedia data fetching capabilities

## Architecture

```
User Query → API → Retriever → Generator → Formatted Response
     ↑                                          ↓
Document Store ← Indexer ← Document Processor ← Sources
```

## Tech Stack

- **Language**: Python 3.10+
- **Embedding Models**: sentence-transformers (all-MiniLM-L6-v2)
- **Generator Models**: Hugging Face models (flan-t5-base)
- **Vector DB**: FAISS
- **Web API**: FastAPI
- **Frontend**: HTML + JavaScript
- **Deployment**: Docker

## Project Structure

```
src/
├── rag_system/
│   ├── data/              # Data ingestion and preprocessing
│   ├── models/            # Embedding and generation models
│   ├── api/               # FastAPI application
│   ├── frontend/          # Web UI
│   ├── rag_pipeline.py    # Main RAG pipeline
├── requirements.txt       # Python dependencies
Dockerfile                 # Docker configuration
docker-compose.yml         # Docker Compose configuration
```

## Setup

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Wikipedia-API library:
   ```bash
   pip install wikipedia-api
   ```

### Usage

#### Option 1: Using Python directly

1. Start the API server:
   ```bash
   cd src/rag_system
   python api/main.py
   ```

2. Access the web UI at `http://localhost:8000/frontend/index.html`

3. Use the API endpoints:
   - POST `/query` - Query the RAG system
   - POST `/add_documents` - Add documents to the system
   - POST `/build_index` - Build the search index

#### Option 2: Using Docker

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the web UI at `http://localhost:8000`

3. The system will automatically initialize with sample data on first run

##### Docker Troubleshooting

If you encounter issues with the Docker deployment:

1. Check container logs:
   ```bash
   docker-compose logs --tail=50
   ```

2. Verify the containers are running:
   ```bash
   docker-compose ps
   ```

3. For detailed troubleshooting, see [TROUBLESHOOTING_DOCKER.md](TROUBLESHOOTING_DOCKER.md)

4. If ports are conflicting, modify the port mapping in `docker-compose.yml`

## Wikipedia Integrations

The system includes multiple ways to fetch and integrate Wikipedia content:

### 1. Featured Article Integration
- **Daily Updates**: Automatically fetch today's featured article
- **Historical Context**: Get historical events that happened today
- **Seamless Integration**: Add featured articles directly to the RAG system
- **Query Support**: Ask questions about the featured content

For detailed information, see [README_FEATURED_ARTICLE.md](README_FEATURED_ARTICLE.md)

### 2. Wikipedia-API Library Integration
- **Comprehensive Data**: Access to sections, links, categories
- **Structured Information**: Better organized page content
- **Advanced Features**: Detailed page analysis capabilities
- **RAG Integration**: Format content for direct use with RAG system

## API Endpoints

### Query the RAG System

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Who led the Salt Satyagraha in 1930 and why was it important?"}'
```

### Add Documents

```bash
curl -X POST "http://localhost:8000/add_documents" \
     -H "Content-Type: application/json" \
     -d '[{"id": "doc1", "title": "Gandhi - Salt March", "source_url": "https://example.com/salt-march", "text": "Mahatma Gandhi led the Salt Satyagraha in 1930..."}]'
```

### Build Index

```bash
curl -X POST "http://localhost:8000/build_index"
```

## Development

### Adding New Documents

To add new documents to the RAG system:

1. Prepare documents in JSON format with fields: `id`, `title`, `source_url`, `text`
2. Use the `/add_documents` endpoint to add them
3. Use the `/build_index` endpoint to rebuild the search index

### Customizing Models

You can customize the embedding and generation models by modifying the model names in:
- [models/embedding_manager.py](src/rag_system/models/embedding_manager.py)
- [models/generator.py](src/rag_system/models/generator.py)

## Deployment

### Cloud Deployment Options

1. **AWS**: Deploy with AWS ECS or Lambda + API Gateway
2. **Render**: Deploy using Render's web service
3. **Heroku**: Deploy using Heroku's container registry
4. **GCP**: Deploy with Google Cloud Run

### Environment Variables

- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 8000)

## Example Usage

Input:
```
"Who led the Salt Satyagraha in 1930 and why was it important?"
```

Output:
```json
{
  "question": "Who led the Salt Satyagraha in 1930 and why was it important?",
  "answer": "Mahatma Gandhi led the Salt Satyagraha (Salt March) in 1930. He marched from Sabarmati to Dandi to protest the British monopoly and salt tax. The movement became a pivotal act of non-violent civil disobedience that mobilized mass participation across India and highlighted the injustice of colonial laws.",
  "sources": [
    {
      "title": "Gandhi - Salt March",
      "source_url": "https://example.com/salt-march",
      "score": 0.2345
    },
    {
      "title": "Salt Act",
      "source_url": "https://example.com/salt-act",
      "score": 0.3456
    }
  ]
}
```

## Evaluation & Quality Control

- **Retrieval**: Recall@k metrics
- **Generation**: ROUGE/BLEU scores
- **Faithfulness**: Check if generated claims exist in retrieved passages
- **Human evaluation**: Rate answers for accuracy and helpfulness

## Future Improvements

- Interactive provenance (click sentences to see source passages)
- Multi-lingual support
- Conversational RAG (maintain chat history)
- Hybrid retrieval (BM25 + dense embeddings)
- Explainability features

## License

This project is licensed under the MIT License.