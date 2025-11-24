"""
Quick initialization script for the RAG system.
This script sets up the RAG system with minimal data for testing.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def quick_initialize():
    """Quickly initialize the RAG system with minimal data."""
    
    # Create RAG system instance
    rag_system = RAGSystem()
    
    # Minimal sample document
    sample_documents = [
        {
            "id": "test_doc_1",
            "title": "Test Document",
            "source_url": "https://example.com/test",
            "text": "This is a test document to verify that the RAG system is working correctly. The system should be able to retrieve this document when queried about test content."
        }
    ]
    
    print("Adding test document to the RAG system...")
    rag_system.add_documents(sample_documents)
    
    print("Building index...")
    rag_system.build_index()
    
    print("RAG system initialized with test data!")
    
    # Test a sample query
    print("\nTesting with a sample query...")
    try:
        result = rag_system.query("What is this document about?")
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for source in result['sources']:
            print(f"  - {source['title']} ({source['source_url']})")
    except Exception as e:
        print(f"Error during test query: {e}")


if __name__ == "__main__":
    quick_initialize()