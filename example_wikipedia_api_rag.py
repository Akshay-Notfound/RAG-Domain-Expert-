"""
Example script demonstrating how to use the Wikipedia-API library with the RAG system.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.wikipedia_api_fetcher import WikipediaApiFetcher
from src.rag_system.rag_pipeline import RAGSystem


def main():
    """Demonstrate using the Wikipedia-API library with the RAG system."""
    print("Integrating Wikipedia-API with RAG system")
    print("=" * 50)
    
    # Initialize components
    fetcher = WikipediaApiFetcher()
    rag_system = RAGSystem()
    
    # Fetch a Wikipedia page
    title = "Machine learning"
    print(f"Fetching Wikipedia page: {title}")
    
    # Format as RAG document
    document = fetcher.format_page_as_document(title)
    
    if not document:
        print(f"Could not fetch page: {title}")
        return
    
    print(f"Successfully fetched: {document['title']}")
    print(f"URL: {document['source_url']}")
    print(f"Content length: {len(document['text'])} characters")
    
    # Add the document to the RAG system
    print("\nAdding document to RAG system...")
    rag_system.add_documents([document])
    
    # Build the index
    print("Building index...")
    rag_system.build_index()
    
    # Query the system about the document
    print("\nQuerying the RAG system...")
    questions = [
        f"What is {title}?",
        "What are the applications of machine learning?",
        "Who are some pioneers in machine learning?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 30)
        try:
            result = rag_system.query(question)
            print(f"Answer: {result['answer']}")
            if result['sources']:
                source = result['sources'][0]
                print(f"Source: {source['title']}")
        except Exception as e:
            print(f"Error querying: {e}")


if __name__ == "__main__":
    main()