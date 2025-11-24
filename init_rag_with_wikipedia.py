"""
Initialize the RAG system with sample documents and Wikipedia articles.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem
from rag_system.data.wikipedia_fetcher import WikipediaFetcher

def init_rag_system():
    """Initialize the RAG system with sample documents and Wikipedia articles."""
    print("Initializing RAG system...")
    
    # Create RAG system instance
    rag_system = RAGSystem()
    
    # Add some sample documents
    sample_docs = [
        {
            "id": "doc_1",
            "title": "Gandhi - Salt March",
            "source_url": "https://example.com/salt-march",
            "text": "Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax. The movement became a pivotal act of non-violent civil disobedience that mobilized mass participation across India and highlighted the injustice of colonial laws."
        },
        {
            "id": "doc_2",
            "title": "Salt Act",
            "source_url": "https://example.com/salt-act",
            "text": "The Salt Act prohibited Indians from collecting or selling salt. This law was a key source of revenue for the British colonial government and was deeply resented by the Indian population. Gandhi's march was a direct challenge to this unjust law."
        }
    ]
    
    print("Adding sample documents...")
    rag_system.add_documents(sample_docs)
    
    # Fetch some Wikipedia articles
    print("Fetching Wikipedia articles...")
    wikipedia_fetcher = WikipediaFetcher()
    wikipedia_docs = wikipedia_fetcher.search_and_fetch_articles("Artificial Intelligence", 2)
    
    if wikipedia_docs:
        print(f"Adding {len(wikipedia_docs)} Wikipedia articles...")
        rag_system.add_documents(wikipedia_docs)
    else:
        print("No Wikipedia articles fetched.")
    
    # Build the index
    print("Building index...")
    rag_system.build_index()
    
    print("RAG system initialized successfully!")

if __name__ == "__main__":
    init_rag_system()