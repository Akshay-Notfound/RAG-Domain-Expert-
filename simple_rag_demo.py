"""
Simple RAG Demo - A very basic demonstration of RAG concepts
"""

import re
from typing import List, Dict, Any


class SimpleRAG:
    """A simple RAG system that demonstrates the core concepts."""
    
    def __init__(self):
        self.documents = []
        self.processed_chunks = []
    
    def add_document(self, doc_id: str, title: str, content: str, source: str = ""):
        """Add a document to the system."""
        document = {
            "id": doc_id,
            "title": title,
            "content": content,
            "source": source
        }
        self.documents.append(document)
        print(f"Added document: {title}")
    
    def process_documents(self):
        """Process documents into chunks (simplified)."""
        self.processed_chunks = []
        for doc in self.documents:
            # For simplicity, we'll use the entire document as one chunk
            chunk = {
                "id": f"{doc['id']}_chunk_0",
                "text": doc["content"],
                "title": doc["title"],
                "source": doc["source"],
                "doc_id": doc["id"]
            }
            self.processed_chunks.append(chunk)
        print(f"Processed {len(self.documents)} documents into {len(self.processed_chunks)} chunks")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Simple keyword-based search."""
        query_words = set(query.lower().split())
        results = []
        
        for chunk in self.processed_chunks:
            text_words = set(chunk["text"].lower().split())
            # Simple scoring based on word overlap
            score = len(query_words.intersection(text_words))
            if score > 0:
                result = chunk.copy()
                result["score"] = score
                results.append(result)
        
        # Sort by score (higher is better)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def generate_response(self, query: str, relevant_chunks: List[Dict[str, Any]]) -> str:
        """Generate a simple response based on relevant chunks."""
        if not relevant_chunks:
            return "I don't have enough information to answer that question."
        
        # Create a simple response using the most relevant chunk
        top_chunk = relevant_chunks[0]
        context = top_chunk["text"][:300] + "..." if len(top_chunk["text"]) > 300 else top_chunk["text"]
        
        return f"Based on the document '{top_chunk['title']}': {context}"
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a query through the RAG system."""
        print(f"\nProcessing query: '{question}'")
        
        # Retrieve relevant documents
        relevant_chunks = self.search(question)
        print(f"Found {len(relevant_chunks)} relevant chunks")
        
        # Generate response
        answer = self.generate_response(question, relevant_chunks)
        
        # Format sources
        sources = [
            {
                "title": chunk["title"],
                "source": chunk["source"],
                "score": chunk["score"]
            }
            for chunk in relevant_chunks
        ]
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }


def main():
    """Demonstrate the simple RAG system."""
    print("=== Simple RAG System Demo ===")
    
    # Create RAG system
    rag = SimpleRAG()
    
    # Add sample documents about the Salt March
    rag.add_document(
        doc_id="salt_march",
        title="Gandhi's Salt March",
        content="Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax. The 24-day march covered 240 miles and became a pivotal act of non-violent civil disobedience. This movement mobilized mass participation across India and highlighted the injustice of colonial laws. The Salt March began on March 12, 1930, and ended on April 5, 1930, when Gandhi picked up a handful of salt from the Arabian Sea, symbolically violating the Salt Act.",
        source="https://example.com/history/india/salt-march"
    )
    
    rag.add_document(
        doc_id="salt_act",
        title="The Salt Act of 1882",
        content="The Salt Act prohibited Indians from collecting or selling salt, a basic necessity. This law was a key source of revenue for the British colonial government and was deeply resented by the Indian population. The tax on salt was seen as a symbol of British exploitation. The Act gave the British government a monopoly on the production and sale of salt, forcing Indians to buy expensive, imported salt instead of making their own.",
        source="https://example.com/history/india/salt-act"
    )
    
    rag.add_document(
        doc_id="independence",
        title="Indian Independence Movement",
        content="The Indian independence movement was a series of activities aimed at ending British rule in India. It spanned over 90 years and involved various forms of resistance, from non-violent civil disobedience to armed rebellion. Key figures included Mahatma Gandhi, Jawaharlal Nehru, Subhas Chandra Bose, and Sardar Patel. The movement culminated in India's independence on August 15, 1947. The Salt March of 1930 was one of the most significant events in this movement.",
        source="https://example.com/history/india/independence"
    )
    
    # Process documents
    rag.process_documents()
    
    # Test queries
    test_queries = [
        "Who led the Salt Satyagraha in 1930?",
        "What was the purpose of the Salt March?",
        "When did India gain independence?"
    ]
    
    print("\n=== Running Test Queries ===")
    for query in test_queries:
        result = rag.query(query)
        print(f"\nQuestion: {result['question']}")
        print(f"Answer: {result['answer']}")
        print("Sources:")
        for source in result['sources']:
            print(f"  - {source['title']} (Relevance: {source['score']})")
        print("-" * 50)


if __name__ == "__main__":
    main()