"""
Script to query the RAG system about Wikipedia's featured article.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.rag_pipeline import RAGSystem


def main():
    """Query the RAG system about the featured article."""
    if len(sys.argv) < 2:
        print("Usage: python query_featured_article.py <question>")
        print("Example: python query_featured_article.py 'What happened in the featured article?'")
        return False
    
    question = ' '.join(sys.argv[1:])
    
    # Initialize the RAG system
    try:
        rag_system = RAGSystem()
        rag_system.load_retriever()
    except FileNotFoundError:
        print("RAG system not initialized. Please run the update script first.")
        return False
    except Exception as e:
        print(f"Error loading RAG system: {e}")
        return False
    
    # Query the system
    print(f"Question: {question}")
    print("-" * 50)
    
    try:
        result = rag_system.query(question)
        print(f"Answer: {result['answer']}")
        print("-" * 50)
        print("Sources:")
        for i, source in enumerate(result['sources'], 1):
            print(f"{i}. {source['title']}")
            print(f"   URL: {source['source_url']}")
            print(f"   Score: {source['score']:.4f}")
            print()
    except Exception as e:
        print(f"Error querying RAG system: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()