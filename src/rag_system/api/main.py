"""
FastAPI application for the RAG system.
Provides RESTful endpoints for querying the RAG system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import json

# Add project `src` directory to path so package imports work
# (ensures `rag_system` is recognized as a package and relative imports succeed)
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from rag_system.rag_pipeline import RAGSystem
from rag_system.data.wikipedia_fetcher import WikipediaFetcher


def load_api_config():
    """Load API configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "api_host": "0.0.0.0",
            "api_port": 8000
        }


# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class WikipediaQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    wikipedia_results: Optional[int] = 3


class Source(BaseModel):
    title: str
    source_url: str
    score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]


# Global instances
rag_system: Optional[RAGSystem] = None
wikipedia_fetcher: Optional[WikipediaFetcher] = None

# Initialize FastAPI app
app = FastAPI(
    title="RAG System API",
    description="API for querying the Retrieval-Augmented Generation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Static file serving is handled separately by the frontend server


def ensure_rag_system_loaded():
    """Lazily initialize the RAG system when first needed.

    This avoids importing heavy ML libraries at server startup so the API
    can come up quickly. The first request that requires the RAG system
    will block while models load.
    """
    global rag_system, wikipedia_fetcher
    if rag_system is None:
        print("Initializing RAG system (this may take some time)...")
        # Set correct paths for data and indexes directories
        project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        data_dir = os.path.join(project_root, 'data')
        indexes_dir = os.path.join(project_root, 'indexes')
        rag_system = RAGSystem(data_dir=data_dir, indexes_dir=indexes_dir)
        
        # Initialize Wikipedia fetcher
        wikipedia_fetcher = WikipediaFetcher()

        # Attempt to load an existing retriever if index files exist
        try:
            if os.path.exists(rag_system.chunks_file) and os.path.exists(rag_system.metadata_file):
                print("Loading existing index...")
                rag_system.load_retriever()
        except Exception as exc:
            print(f"Warning: failed to load retriever on init: {exc}")

    return rag_system


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system.
    
    Args:
        request: Query request containing the question and top_k parameter
        
    Returns:
        Query response with answer and sources
    """
    # Ensure RAG system is initialized (may block on first call)
    rag = ensure_rag_system_loaded()

    # Query the RAG system
    result = rag.query(request.query, request.top_k)
    
    # Convert to response model
    response = QueryResponse(
        question=result["question"],
        answer=result["answer"],
        sources=[
            Source(
                title=source["title"],
                source_url=source["source_url"],
                score=source["score"]
            )
            for source in result["sources"]
        ]
    )
    
    return response


@app.post("/query_with_wikipedia", response_model=QueryResponse)
async def query_with_wikipedia(request: WikipediaQueryRequest):
    """
    Query the RAG system with additional Wikipedia context.
    
    Args:
        request: Query request with Wikipedia integration options
        
    Returns:
        Query response with answer and sources
    """
    global rag_system, wikipedia_fetcher
    
    # Ensure systems are initialized
    rag = ensure_rag_system_loaded()
    
    # Fetch Wikipedia articles
    if wikipedia_fetcher is None:
        wikipedia_fetcher = WikipediaFetcher()
    
    wikipedia_docs = wikipedia_fetcher.search_and_fetch_articles(
        request.query, 
        request.wikipedia_results or 3
    )
    
    # Add Wikipedia documents to RAG system temporarily
    if wikipedia_docs:
        original_docs = []
        # Save original documents if needed
        # Add Wikipedia documents
        rag.add_documents(wikipedia_docs)
        # Rebuild index
        rag.build_index()
        rag.load_retriever()
    
    # Query the RAG system
    result = rag.query(request.query, request.top_k)
    
    # Convert to response model
    response = QueryResponse(
        question=result["question"],
        answer=result["answer"],
        sources=[
            Source(
                title=source["title"],
                source_url=source["source_url"],
                score=source["score"]
            )
            for source in result["sources"]
        ]
    )
    
    return response


@app.post("/add_documents")
async def add_documents(documents: List[dict]):
    """
    Add documents to the RAG system.
    
    Args:
        documents: List of document dictionaries
        
    Returns:
        Status message
    """
    rag = ensure_rag_system_loaded()
    rag.add_documents(documents)
    return {"message": f"Added {len(documents)} documents"}


@app.post("/build_index")
async def build_index():
    """
    Build the FAISS index from added documents.
    
    Returns:
        Status message
    """
    rag = ensure_rag_system_loaded()
    rag.build_index()
    rag.load_retriever()
    return {"message": "Index built successfully"}


# API root endpoint
@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {"message": "RAG System API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "RAG System is running"}


if __name__ == "__main__":
    import uvicorn
    
    # Load API configuration
    api_config = load_api_config()
    host = api_config.get("api_host", "0.0.0.0")
    port = api_config.get("api_port", 8000)
    
    uvicorn.run(app, host=host, port=port)