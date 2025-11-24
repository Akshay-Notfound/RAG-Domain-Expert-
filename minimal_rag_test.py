"""
Minimal RAG test to verify the system is working.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem

def test_minimal_rag():
    """Test the RAG system with minimal setup."""
    try:
        print("Testing minimal RAG system...")
        
        # Create a very simple RAG system
        rag_system = RAGSystem()
        
        # Add a simple document
        sample_docs = [
            {
                "id": "test_doc_1",
                "title": "Test Document",
                "source_url": "https://example.com/test",
                "text": "This is a test document to verify that the RAG system is working correctly. The system should be able to retrieve this document when queried about test content."
            }
        ]
        
        print("Adding documents...")
        rag_system.add_documents(sample_docs)
        
        print("Building index...")
        rag_system.build_index()
        
        print("Loading retriever...")
        rag_system.load_retriever()
        
        print("Testing query...")
        result = rag_system.query("What is this document about?")
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for source in result['sources']:
            print(f"  - {source['title']} ({source['source_url']})")
            
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_minimal_rag()