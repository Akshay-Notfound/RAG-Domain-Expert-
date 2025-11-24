"""
Script to update the RAG system with Wikipedia's featured article of the day.
This can be run daily to keep the RAG system updated with fresh content.
"""

import os
import sys
import json
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher
from src.rag_system.rag_pipeline import RAGSystem


def load_existing_documents(chunks_file: str) -> list:
    """
    Load existing documents from the chunks file.
    
    Args:
        chunks_file: Path to the chunks file
        
    Returns:
        List of existing documents
    """
    documents = []
    if os.path.exists(chunks_file):
        # Read the metadata file to get document IDs
        metadata_file = chunks_file.replace('chunks.jsonl', 'metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                # Extract unique document IDs from metadata
                doc_ids = set()
                for chunk_meta in metadata:
                    doc_id = chunk_meta.get('document_id', '').split('_')[0]  # Extract base document ID
                    if doc_id.startswith('wikipedia_'):
                        doc_ids.add(doc_id)
                documents = list(doc_ids)
    return documents


def main():
    """Update the RAG system with today's featured Wikipedia article."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating RAG system with today's featured article...")
    
    # Initialize components
    fetcher = FeaturedArticleFetcher()
    rag_system = RAGSystem()
    
    # Check if we already have today's featured article
    featured_doc = fetcher.fetch_featured_article_as_document()
    
    if not featured_doc:
        print("Failed to fetch today's featured article.")
        return False
    
    print(f"Successfully fetched: {featured_doc['title']}")
    
    # Check if this document is already in the system
    existing_docs = load_existing_documents(rag_system.chunks_file)
    
    if featured_doc['id'] in existing_docs:
        print("This article is already in the RAG system. Skipping update.")
        return True
    
    # Add the new document to the RAG system
    print("Adding featured article to RAG system...")
    rag_system.add_documents([featured_doc])
    
    # Rebuild the index
    print("Rebuilding index...")
    rag_system.build_index()
    
    print("RAG system successfully updated with today's featured article!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)