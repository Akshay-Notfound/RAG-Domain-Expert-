"""
Main RAG System Pipeline
Integrates all components of the RAG system.
"""

import os
import json
from typing import List, Dict, Any, Optional
from .data.document_processor import DocumentProcessor
from .models.embedding_manager import EmbeddingManager
from .models.retriever import Retriever
from .models.generator import Generator


def load_config():
    """Load configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "embedding_model": "all-MiniLM-L6-v2",
            "generation_model": "google/flan-t5-base",
            "chunk_size": 500,
            "chunk_overlap": 50,
            "default_top_k": 5,
            "max_new_tokens": 256
        }


class SimpleRetriever:
    """A simple retriever that works without FAISS index."""
    
    def __init__(self, chunks_metadata: List[Dict[str, Any]]):
        self.chunks_metadata = chunks_metadata
        # Load chunks from the chunks file
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        chunks_file = os.path.join(data_dir, 'chunks.jsonl')
        self.chunks = []
        if os.path.exists(chunks_file):
            with open(chunks_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.chunks.append(json.loads(line.strip()))
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search."""
        query_words = set(query.lower().split())
        results = []
        
        for chunk in self.chunks:
            text_words = set(chunk["text"].lower().split())
            # Simple scoring based on word overlap
            score = len(query_words.intersection(text_words))
            if score > 0:
                result = chunk.copy()
                result["score"] = score
                results.append(result)
        
        # Sort by score (higher is better) and return top k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]
    
    def format_context(self, passages: List[Dict[str, Any]]) -> str:
        """Format passages as context for generation."""
        if not passages:
            return "No relevant information found."
        
        context_parts = []
        for passage in passages:
            title = passage.get('title', 'Unknown')
            text = passage.get('text', '')
            context_parts.append(f"Document: {title}\nContent: {text}")
        
        return "\n\n".join(context_parts)


class RAGSystem:
    """Main RAG system that integrates all components."""
    
    def __init__(self, data_dir: str = "data", indexes_dir: str = "indexes"):
        """
        Initialize the RAG system.
        
        Args:
            data_dir: Directory for storing data files
            indexes_dir: Directory for storing index files
        """
        self.data_dir = data_dir
        self.indexes_dir = indexes_dir
        
        # Create directories if they don't exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(indexes_dir, exist_ok=True)
        
        # Load configuration
        self.config = load_config()
        
        # Initialize components
        self.document_processor = DocumentProcessor(
            chunk_size=self.config["chunk_size"],
            overlap=self.config["chunk_overlap"]
        )
        self.embedding_manager = EmbeddingManager(
            model_name=self.config["embedding_model"]
        )
        self.retriever: Optional[SimpleRetriever] = None
        self.generator = Generator(
            model_name=self.config["generation_model"],
            api_key=self.config.get("google_api_key")
        )
        
        # File paths
        self.chunks_file = os.path.join(data_dir, "chunks.jsonl")
        self.index_file = os.path.join(indexes_dir, "faiss.index")
        self.metadata_file = os.path.join(data_dir, "metadata.json")
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents to the RAG system.
        
        Args:
            documents: List of document dictionaries with 'text', 'title', 'source_url'
        """
        all_chunks = []
        
        for i, doc in enumerate(documents):
            doc_id = doc.get('id', f'doc_{i}')
            title = doc.get('title', '')
            source_url = doc.get('source_url', '')
            text = doc.get('text', '')
            
            # Process document
            chunks = self.document_processor.chunk_text(
                text=text,
                doc_id=doc_id,
                title=title,
                source_url=source_url
            )
            
            all_chunks.extend(chunks)
        
        # Save chunks
        self.document_processor.save_chunks(all_chunks, self.chunks_file)
        print(f"Processed {len(documents)} documents into {len(all_chunks)} chunks")
    
    def build_index(self):
        """Build a simple index (just confirms files exist)."""
        if not os.path.exists(self.chunks_file):
            raise FileNotFoundError(f"Chunks file not found: {self.chunks_file}")
        
        print("Index building simulated - using simple retrieval")
    
    def load_retriever(self):
        """Load the simple retriever with the chunks."""
        if not os.path.exists(self.chunks_file):
            raise FileNotFoundError("Chunks file not found. Please add documents first.")
        
        # Load metadata
        chunks_metadata = []
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                chunks_metadata = json.load(f)
        
        # Initialize simple retriever
        self.retriever = SimpleRetriever(chunks_metadata)
        
        print("Simple retriever loaded successfully")
    
    def query(self, question: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: User question
            top_k: Number of passages to retrieve (uses default if not specified)
            
        Returns:
            Dictionary with answer and sources
        """
        if top_k is None:
            top_k = self.config.get("default_top_k", 5)
            
        # Ensure top_k is an integer
        top_k = int(top_k) if top_k is not None else 5
            
        if self.retriever is None:
            self.load_retriever()
        
        # This check satisfies the type checker
        if self.retriever is None:
            raise RuntimeError("Failed to load retriever")
        
        # Retrieve relevant passages
        passages = self.retriever.search(question, k=top_k)
        
        # Format context
        context = self.retriever.format_context(passages)
        
        # Generate answer
        max_new_tokens = self.config.get("max_new_tokens", 256)
        answer = self.generator.generate_answer(context, question, max_new_tokens=max_new_tokens)
        
        # Process tags
        used_general_knowledge = False
        if "[GENERAL_KNOWLEDGE]" in answer:
            used_general_knowledge = True
            answer = answer.replace("[GENERAL_KNOWLEDGE]", "").strip()
        elif "[USED_CONTEXT]" in answer:
            answer = answer.replace("[USED_CONTEXT]", "").strip()
            
        # Prepare response
        response = {
            "question": question,
            "answer": answer,
            "sources": [],
            "used_passages": passages
        }
        
        # Only include sources if general knowledge was NOT used
        if not used_general_knowledge:
            response["sources"] = [
                {
                    "title": p.get('title', ''),
                    "source_url": p.get('source_url', ''),
                    "score": p.get('score', 0)
                }
                for p in passages
            ]
        
        return response


# Example usage
if __name__ == "__main__":
    # Example of how to use the RAGSystem
    rag_system = RAGSystem()
    
    # Sample documents
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
    
    # Add documents
    rag_system.add_documents(sample_docs)
    
    # Build index
    rag_system.build_index()
    
    # Query system
    result = rag_system.query("Who led the Salt Satyagraha in 1930 and why was it important?")
    print("Question:", result["question"])
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])