"""
Data loader script for the RAG system.
This script helps load documents from various sources into the RAG system.
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def load_documents_from_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """Load documents from a JSONL file."""
    documents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            documents.append(json.loads(line.strip()))
    return documents


def load_documents_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Load documents from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_documents_from_text(file_path: str, title: str = "", source_url: str = "") -> List[Dict[str, Any]]:
    """Load documents from a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create a single document
    document = {
        "id": os.path.basename(file_path),
        "title": title or os.path.basename(file_path),
        "source_url": source_url,
        "text": text
    }
    
    return [document]


def load_documents_from_url(url: str, title: str = "") -> List[Dict[str, Any]]:
    """Load documents from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        document = {
            "id": url,
            "title": title or url,
            "source_url": url,
            "text": response.text
        }
        
        return [document]
    except Exception as e:
        print(f"Error loading document from URL {url}: {e}")
        return []


def add_documents_to_rag(documents: List[Dict[str, Any]], rag_system: Optional[RAGSystem] = None) -> RAGSystem:
    """Add documents to the RAG system and rebuild the index."""
    if rag_system is None:
        rag_system = RAGSystem()
    
    print(f"Adding {len(documents)} documents to the RAG system...")
    rag_system.add_documents(documents)
    
    print("Building index...")
    rag_system.build_index()
    
    print("Documents added successfully!")
    return rag_system


def main():
    """Main function to demonstrate loading documents."""
    print("RAG System Data Loader")
    print("======================")
    
    # Example usage
    rag_system = RAGSystem()
    
    # Sample documents (in practice, you would load these from files or URLs)
    sample_documents = [
        {
            "id": "sample_1",
            "title": "Sample Document 1",
            "source_url": "https://example.com/doc1",
            "text": "This is a sample document for demonstration purposes."
        },
        {
            "id": "sample_2",
            "title": "Sample Document 2",
            "source_url": "https://example.com/doc2",
            "text": "This is another sample document with different content."
        }
    ]
    
    # Add documents to RAG system
    add_documents_to_rag(sample_documents, rag_system)
    
    # Test query
    print("\nTesting with a sample query...")
    result = rag_system.query("What is this document about?")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()