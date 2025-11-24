"""
Minimal RAG System - A simplified version that demonstrates the core concepts
without requiring heavy dependencies.
"""

import json
import re
from typing import List, Dict, Any


class SimpleDocumentProcessor:
    """Simple document processor for chunking text."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def chunk_text(self, text: str, doc_id: str, title: str = "", source_url: str = "") -> List[Dict[str, Any]]:
        """Split text into chunks."""
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
            # Ensure we don't go backwards
            if start_pos <= 0 or start_pos >= len(cleaned_text):
                break
            # If the next chunk would be too small, extend it to the end
            if start_pos + self.chunk_size > len(cleaned_text):
                start_pos = len(cleaned_text) - self.chunk_size
                if start_pos < 0:
                    start_pos = 0
                
        return chunks


class SimpleRetriever:
    """Simple retriever that does keyword matching."""
    
    def __init__(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Simple keyword-based search."""
        query_words = set(query.lower().split())
        scored_chunks = []
        
        for chunk in self.chunks:
            text_words = set(chunk["text"].lower().split())
            # Simple scoring based on word overlap
            score = len(query_words.intersection(text_words))
            if score > 0:
                chunk_with_score = chunk.copy()
                chunk_with_score["score"] = score
                scored_chunks.append(chunk_with_score)
        
        # Sort by score and return top k
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:k]
    
    def format_context(self, passages: List[Dict[str, Any]]) -> str:
        """Format retrieved passages into a context string."""
        context_parts = []
        for passage in passages:
            title = passage.get('title', 'Unknown')
            text = passage.get('text', '')
            source = passage.get('source_url', '')
            context_parts.append(f"[{title} | {source}] {text}")
        
        return "\n\n---\n\n".join(context_parts)


class SimpleGenerator:
    """Simple generator that creates template-based responses."""
    
    def generate_answer(self, context: str, query: str) -> str:
        """Generate a simple template-based answer."""
        # In a real implementation, this would use a language model
        # For this minimal version, we'll create a template response
        return f"Based on the provided context about '{query}', here is what I found: \n\n{context[:200]}...\n\nFor more detailed information, please refer to the sources above."


class MinimalRAGSystem:
    """Minimal RAG system that demonstrates the core concepts."""
    
    def __init__(self):
        self.document_processor = SimpleDocumentProcessor()
        self.retriever = None
        self.generator = SimpleGenerator()
        self.chunks = []
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the RAG system."""
        all_chunks = []
        
        for i, doc in enumerate(documents):
            doc_id = doc.get('id', f'doc_{i}')
            title = doc.get('title', '')
            source_url = doc.get('source_url', '')
            text = doc.get('text', '')
            
            chunks = self.document_processor.chunk_text(
                text=text,
                doc_id=doc_id,
                title=title,
                source_url=source_url
            )
            
            all_chunks.extend(chunks)
        
        self.chunks = all_chunks
        print(f"Processed {len(documents)} documents into {len(all_chunks)} chunks")
    
    def build_index(self):
        """Build a simple retriever from processed documents."""
        self.retriever = SimpleRetriever(self.chunks)
        print("Simple retriever built successfully")
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Query the RAG system."""
        if self.retriever is None:
            self.build_index()
        
        # Check if retriever was built successfully
        if self.retriever is None:
            raise RuntimeError("Failed to build retriever")
        
        # Retrieve relevant passages
        passages = self.retriever.search(question, k=top_k)
        
        # Format context
        context = self.retriever.format_context(passages)
        
        # Generate answer
        answer = self.generator.generate_answer(context, question)
        
        # Prepare response
        response = {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "title": p.get('title', ''),
                    "source_url": p.get('source_url', ''),
                    "score": p.get('score', 0)
                }
                for p in passages
            ],
            "used_passages": passages
        }
        
        return response


def main():
    """Main function to demonstrate the minimal RAG system."""
    print("Starting Minimal RAG System...")
    
    # Create RAG system instance
    rag_system = MinimalRAGSystem()
    
    # Sample historical documents about the Salt March
    sample_documents = [
        {
            "id": "salt_march_1",
            "title": "Gandhi's Salt March",
            "source_url": "https://example.com/history/india/salt-march",
            "text": "Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax. The 24-day march covered 240 miles and became a pivotal act of non-violent civil disobedience. This movement mobilized mass participation across India and highlighted the injustice of colonial laws. The Salt March began on March 12, 1930, and ended on April 5, 1930, when Gandhi picked up a handful of salt from the Arabian Sea, symbolically violating the Salt Act."
        },
        {
            "id": "salt_act_1",
            "title": "The Salt Act of 1882",
            "source_url": "https://example.com/history/india/salt-act",
            "text": "The Salt Act prohibited Indians from collecting or selling salt, a basic necessity. This law was a key source of revenue for the British colonial government and was deeply resented by the Indian population. The tax on salt was seen as a symbol of British exploitation. The Act gave the British government a monopoly on the production and sale of salt, forcing Indians to buy expensive, imported salt instead of making their own."
        },
        {
            "id": "independence_movement_1",
            "title": "Indian Independence Movement",
            "source_url": "https://example.com/history/india/independence",
            "text": "The Indian independence movement was a series of activities aimed at ending British rule in India. It spanned over 90 years and involved various forms of resistance, from non-violent civil disobedience to armed rebellion. Key figures included Mahatma Gandhi, Jawaharlal Nehru, Subhas Chandra Bose, and Sardar Patel. The movement culminated in India's independence on August 15, 1947. The Salt March of 1930 was one of the most significant events in this movement."
        }
    ]
    
    print("Adding sample documents to the RAG system...")
    rag_system.add_documents(sample_documents)
    
    print("Building index...")
    rag_system.build_index()
    
    # Test queries
    test_queries = [
        "Who led the Salt Satyagraha in 1930 and why was it important?",
        "What was the Salt Act and how did it affect Indians?",
        "When did the Salt March begin and end?"
    ]
    
    print("\nTesting with sample queries...")
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print('='*50)
        
        result = rag_system.query(query)
        print(f"Answer: {result['answer']}")
        print("\nSources:")
        for source in result['sources']:
            print(f"  - {source['title']} (Score: {source['score']})")


if __name__ == "__main__":
    main()