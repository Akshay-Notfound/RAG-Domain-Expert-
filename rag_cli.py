"""
Command-line interface for the RAG system.
This script provides a CLI for interacting with the RAG system.
"""

import os
import sys
import json
import argparse

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="RAG System CLI")
    parser.add_argument("--data-dir", default="data", help="Data directory")
    parser.add_argument("--indexes-dir", default="indexes", help="Indexes directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("question", help="Question to ask")
    query_parser.add_argument("--top-k", type=int, default=5, help="Number of passages to retrieve")
    
    # Add documents command
    add_parser = subparsers.add_parser("add", help="Add documents to the RAG system")
    add_parser.add_argument("files", nargs="+", help="JSON/JSONL files containing documents")
    
    # Build index command
    subparsers.add_parser("build", help="Build the search index")
    
    # Test command
    subparsers.add_parser("test", help="Run a test query")
    
    args = parser.parse_args()
    
    # Create RAG system instance
    rag_system = RAGSystem(data_dir=args.data_dir, indexes_dir=args.indexes_dir)
    
    if args.command == "query":
        # Query the RAG system
        result = rag_system.query(args.question, top_k=args.top_k)
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("\nSources:")
        for source in result['sources']:
            print(f"  - {source['title']} ({source['source_url']})")
    
    elif args.command == "add":
        # Add documents
        all_documents = []
        for file_path in args.files:
            if file_path.endswith('.jsonl'):
                # Load from JSONL file
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        all_documents.append(json.loads(line.strip()))
            elif file_path.endswith('.json'):
                # Load from JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents = json.load(f)
                    if isinstance(documents, list):
                        all_documents.extend(documents)
                    else:
                        all_documents.append(documents)
        
        print(f"Adding {len(all_documents)} documents...")
        rag_system.add_documents(all_documents)
        print("Documents added successfully!")
    
    elif args.command == "build":
        # Build index
        print("Building index...")
        rag_system.build_index()
        print("Index built successfully!")
        
        # Load retriever
        print("Loading retriever...")
        rag_system.load_retriever()
        print("Retriever loaded successfully!")
    
    elif args.command == "test":
        # Run test with sample data
        sample_documents = [
            {
                "id": "test_1",
                "title": "Test Document",
                "source_url": "https://example.com/test",
                "text": "This is a test document for the RAG system CLI. The RAG system combines retrieval and generation to provide accurate answers based on domain-specific knowledge sources."
            }
        ]
        
        print("Adding test document...")
        rag_system.add_documents(sample_documents)
        
        print("Building index...")
        rag_system.build_index()
        
        print("Loading retriever...")
        rag_system.load_retriever()
        
        print("Running test query...")
        result = rag_system.query("What is the RAG system?")
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("\nSources:")
        for source in result['sources']:
            print(f"  - {source['title']} ({source['source_url']})")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()