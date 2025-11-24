"""
Retriever for the RAG system.
Handles document retrieval using vector similarity search.
"""

import numpy as np
import faiss
import json
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer


class Retriever:
    """Retrieve relevant documents using vector similarity search."""
    
    def __init__(self, index_path: str, chunks_metadata: List[Dict[str, Any]], 
                 embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the retriever.
        
        Args:
            index_path: Path to the FAISS index
            chunks_metadata: List of chunk metadata
            embedding_model_name: Name of the sentence transformer model to use
        """
        self.index = faiss.read_index(index_path)
        self.chunks_metadata = chunks_metadata
        self.embedding_model = SentenceTransformer(embedding_model_name)
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of relevant chunks with scores
        """
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Search
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)
        
        # Prepare results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.chunks_metadata):
                chunk = self.chunks_metadata[idx].copy()
                chunk['score'] = float(distance)
                results.append(chunk)
        
        return results
    
    def format_context(self, passages: List[Dict[str, Any]]) -> str:
        """
        Format retrieved passages into a context string.
        
        Args:
            passages: List of passage dictionaries
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for passage in passages:
            title = passage.get('title', 'Unknown')
            text = passage.get('text', '')
            source = passage.get('source_url', '')
            context_parts.append(f"[{title} | {source}] {text}")
        
        return "\n\n---\n\n".join(context_parts)


# Example usage
if __name__ == "__main__":
    # This would typically be loaded from files
    sample_chunks = [
        {
            "id": "sample_1",
            "text": "Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax.",
            "title": "Gandhi - Salt March",
            "source_url": "https://example.com/salt-march",
            "start_pos": 0,
            "end_pos": 150
        },
        {
            "id": "sample_2",
            "text": "The Salt Act prohibited Indians from collecting or selling salt; Gandhi's march was a civil disobedience movement.",
            "title": "Salt Act",
            "source_url": "https://example.com/salt-act",
            "start_pos": 0,
            "end_pos": 120
        }
    ]
    
    # For demonstration purposes, we'll create a mock index
    # In practice, you would load this from disk
    print("Retriever module ready for use.")