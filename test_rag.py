"""
Test script for the RAG system.
This script runs basic tests to verify the RAG system functionality.
"""

import os
import sys
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def test_rag_system():
    """Test the RAG system with sample data."""
    
    print("Testing RAG System...")
    
    # Create RAG system instance
    rag_system = RAGSystem()
    
    # Sample documents
    sample_documents = [
        {
            "id": "test_doc_1",
            "title": "Test Document 1",
            "source_url": "https://example.com/test1",
            "text": "This is a test document about artificial intelligence and machine learning. Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals."
        },
        {
            "id": "test_doc_2",
            "title": "Test Document 2",
            "source_url": "https://example.com/test2",
            "text": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention."
        }
    ]
    
    # Test adding documents
    print("1. Testing document addition...")
    rag_system.add_documents(sample_documents)
    print("   ✓ Documents added successfully")
    
    # Test building index
    print("2. Testing index building...")
    rag_system.build_index()
    print("   ✓ Index built successfully")
    
    # Test loading retriever
    print("3. Testing retriever loading...")
    rag_system.load_retriever()
    print("   ✓ Retriever loaded successfully")
    
    # Test querying
    print("4. Testing query functionality...")
    result = rag_system.query("What is artificial intelligence?")
    
    # Check if we got a result
    assert "answer" in result, "No answer in result"
    assert "sources" in result, "No sources in result"
    assert len(result["answer"]) > 0, "Empty answer"
    assert len(result["sources"]) > 0, "No sources returned"
    
    print("   ✓ Query successful")
    print(f"   Answer: {result['answer']}")
    
    print("\n✓ All tests passed! RAG system is working correctly.")


if __name__ == "__main__":
    test_rag_system()