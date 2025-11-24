"""
Document processor for the RAG system.
Handles text extraction, cleaning, and chunking of documents.
"""

import os
import json
import uuid
from typing import List, Dict, Any
import re


class DocumentProcessor:
    """Process documents for the RAG system."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of each text chunk in characters
            overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    def chunk_text(self, text: str, doc_id: str, title: str = "", source_url: str = "") -> List[Dict[str, Any]]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
            doc_id: Document identifier
            title: Document title
            source_url: Source URL of the document
            
        Returns:
            List of chunk dictionaries
        """
        cleaned_text = self.clean_text(text)
        chunks = []
        
        start_pos = 0
        chunk_id = 0
        
        while start_pos < len(cleaned_text):
            end_pos = min(start_pos + self.chunk_size, len(cleaned_text))
            chunk_text = cleaned_text[start_pos:end_pos]
            
            chunk = {
                "id": f"{doc_id}_{chunk_id}",
                "text": chunk_text,
                "title": title,
                "source_url": source_url,
                "start_pos": start_pos,
                "end_pos": end_pos
            }
            
            chunks.append(chunk)
            chunk_id += 1
            
            # Move start position by chunk_size minus overlap
            start_pos = end_pos - self.overlap
            if start_pos >= len(cleaned_text):
                break
                
        return chunks
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_path: str):
        """
        Save chunks to a JSONL file.
        
        Args:
            chunks: List of chunk dictionaries
            output_path: Path to save the chunks
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')


# Example usage
if __name__ == "__main__":
    # Example of how to use the DocumentProcessor
    processor = DocumentProcessor(chunk_size=500, overlap=50)
    
    # Sample text
    sample_text = """
    Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax. 
    The Salt Act prohibited Indians from collecting or selling salt; Gandhi's march was a civil disobedience movement.
    This movement became a pivotal act of non-violent civil disobedience that mobilized mass participation across India.
    """
    
    # Process the text
    chunks = processor.chunk_text(
        text=sample_text,
        doc_id="sample_doc_1",
        title="Gandhi - Salt March",
        source_url="https://example.com/salt-march"
    )
    
    # Save chunks
    processor.save_chunks(chunks, "sample_chunks.jsonl")
    
    print(f"Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk['text'][:100]}...")