"""
Embedding manager for the RAG system.
Handles document embedding and vector indexing.
"""

import numpy as np
import faiss
import json
import os
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """Manage document embeddings and vector indexing."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding manager.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        
    def encode_documents(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Encode documents into embeddings.
        
        Args:
            texts: List of text documents to encode
            batch_size: Batch size for encoding
            
        Returns:
            Array of embeddings
        """
        embeddings = self.model.encode(
            texts, 
            batch_size=batch_size, 
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings
    
    def create_index(self, dimension: int) -> faiss.Index:
        """
        Create a FAISS index.
        
        Args:
            dimension: Dimension of the embeddings
            
        Returns:
            FAISS index
        """
        index = faiss.IndexFlatL2(dimension)
        return index
    
    def build_index_from_chunks(self, chunks_file: str, index_path: str) -> Tuple[faiss.Index, List[Dict[str, Any]]]:
        """
        Build a FAISS index from document chunks.
        
        Args:
            chunks_file: Path to the JSONL file containing chunks
            index_path: Path to save the FAISS index
            
        Returns:
            Tuple of (FAISS index, chunk metadata)
        """
        # Load chunks
        chunks = []
        texts = []
        
        with open(chunks_file, 'r', encoding='utf-8') as f:
            for line in f:
                chunk = json.loads(line.strip())
                chunks.append(chunk)
                texts.append(chunk['text'])
        
        # Encode documents
        print(f"Encoding {len(texts)} documents...")
        embeddings = self.encode_documents(texts)
        
        # Create index
        dimension = embeddings.shape[1]
        index = self.create_index(dimension)
        
        # Add embeddings to index
        index.add(embeddings.astype(np.float32))
        
        # Save index
        faiss.write_index(index, index_path)
        print(f"Index saved to {index_path}")
        
        return index, chunks
    
    def load_index(self, index_path: str) -> faiss.Index:
        """
        Load a FAISS index from disk.
        
        Args:
            index_path: Path to the FAISS index
            
        Returns:
            FAISS index
        """
        return faiss.read_index(index_path)


# Example usage
if __name__ == "__main__":
    # Example of how to use the EmbeddingManager
    embedding_manager = EmbeddingManager()
    
    # For demonstration, we'll create a sample chunks file
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
    
    # Save sample chunks
    with open("sample_chunks.jsonl", "w") as f:
        for chunk in sample_chunks:
            f.write(json.dumps(chunk) + "\n")
    
    # Build index
    index, chunks_metadata = embedding_manager.build_index_from_chunks(
        chunks_file="sample_chunks.jsonl",
        index_path="sample_index.faiss"
    )
    
    print(f"Built index with {index.ntotal} vectors")