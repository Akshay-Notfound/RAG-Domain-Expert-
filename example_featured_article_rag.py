"""
Example script demonstrating how to use the FeaturedArticleFetcher with the RAG system.
"""

import sys
import os

# Add the src directory to the path so we can import the RAG system
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher
from src.rag_system.rag_pipeline import RAGSystem


def main():
    """Demonstrate using the featured article fetcher with the RAG system."""
    print("Fetching today's featured article from Wikipedia...")
    
    # Initialize the featured article fetcher
    fetcher = FeaturedArticleFetcher()
    
    # Fetch today's featured article
    featured_doc = fetcher.fetch_featured_article_as_document()
    
    if not featured_doc:
        print("Could not fetch today's featured article.")
        return
    
    print(f"Successfully fetched: {featured_doc['title']}")
    print(f"URL: {featured_doc['source_url']}")
    print(f"Content preview: {featured_doc['text'][:200]}...")
    
    # Initialize the RAG system
    rag_system = RAGSystem()
    
    # Add the featured article to the RAG system
    print("\nAdding featured article to RAG system...")
    rag_system.add_documents([featured_doc])
    
    # Build the index
    print("Building index...")
    rag_system.build_index()
    
    # Query the system about the featured article
    print("\nQuerying the RAG system about the featured article...")
    question = f"What is the article about {featured_doc['title']} about?"
    result = rag_system.query(question)
    
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['sources'])} found")
    
    # Another example query
    print("\nAsking another question...")
    question = "What are the key points of this article?"
    result = rag_system.query(question)
    
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()