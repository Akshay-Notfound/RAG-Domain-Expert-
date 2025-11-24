"""
Simple test script to verify the RAG system is working.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem

def test_rag():
    """Test the RAG system with a simple query."""
    try:
        # Initialize RAG system with correct paths
        project_root = os.path.dirname(__file__)
        data_dir = os.path.join(project_root, 'data')
        indexes_dir = os.path.join(project_root, 'indexes')
        
        print(f"Project root: {project_root}")
        print(f"Data directory: {data_dir}")
        print(f"Indexes directory: {indexes_dir}")
        
        # Check if data files exist
        chunks_file = os.path.join(data_dir, 'chunks.jsonl')
        metadata_file = os.path.join(data_dir, 'metadata.json')
        
        print(f"Chunks file exists: {os.path.exists(chunks_file)}")
        print(f"Metadata file exists: {os.path.exists(metadata_file)}")
        
        if os.path.exists(chunks_file):
            print("Chunks file content:")
            with open(chunks_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Number of lines: {len(lines)}")
                if lines:
                    print(f"First line: {lines[0][:100]}...")
        
        # Initialize RAG system
        rag_system = RAGSystem(data_dir=data_dir, indexes_dir=indexes_dir)
        
        # Try to load retriever
        print("Loading retriever...")
        rag_system.load_retriever()
        
        # Test a simple query
        print("Testing query...")
        result = rag_system.query("Who led the Salt Satyagraha?")
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for source in result['sources']:
            print(f"  - {source['title']} ({source['source_url']})")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag()