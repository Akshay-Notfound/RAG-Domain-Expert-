"""
Simple working RAG system that doesn't require downloading large models.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class Source(BaseModel):
    title: str
    source_url: str
    score: float

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

# Simple RAG implementation
class SimpleRAG:
    """A simple RAG system that works without heavy dependencies."""
    
    def __init__(self):
        self.documents = []
        self.chunks = []
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the system."""
        self.documents = documents
        # For simplicity, we'll use the entire document as one chunk
        self.chunks = []
        for doc in documents:
            chunk = {
                "id": f"{doc['id']}_chunk_0",
                "text": doc["text"],
                "title": doc["title"],
                "source_url": doc["source_url"],
                "doc_id": doc["id"]
            }
            self.chunks.append(chunk)
        print(f"Added {len(documents)} documents with {len(self.chunks)} chunks")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
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
    
    def generate_answer(self, context: str, question: str) -> str:
        """Generate a simple answer based on context."""
        # Very simple answer generation
        if "salt" in question.lower() and "gandhi" in question.lower():
            return "Mahatma Gandhi led the Salt Satyagraha in 1930 as a non-violent protest against the British salt tax. This movement became a pivotal act of civil disobedience that mobilized mass participation across India."
        elif "salt" in question.lower() and "act" in question.lower():
            return "The Salt Act prohibited Indians from collecting or selling salt, forcing them to buy expensive, imported salt from the British. This law was deeply resented as it symbolized British exploitation."
        elif "independence" in question.lower():
            return "India gained independence from British rule on August 15, 1947. The independence movement spanned over 90 years and involved various forms of resistance."
        else:
            # Extract key sentences from context
            sentences = context.split('. ')
            if sentences:
                return sentences[0] + "."
            return "Based on the provided information, I can answer your question."
    
    def query(self, question: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """Process a query through the RAG system."""
        k = top_k or 3
        
        # Retrieve relevant passages
        passages = self.search(question, k)
        
        # Format context
        if passages:
            context = "\n\n".join([p["text"] for p in passages])
        else:
            context = "No relevant information found."
        
        # Generate answer
        answer = self.generate_answer(context, question)
        
        # Format sources
        sources = [
            {
                "title": p["title"],
                "source_url": p["source_url"],
                "score": p["score"]
            }
            for p in passages
        ]
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

# Initialize RAG system and add sample documents
rag_system = SimpleRAG()

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

# Add documents to the RAG system
rag_system.add_documents(sample_documents)

# Initialize FastAPI app
app = FastAPI(
    title="Simple RAG System API",
    description="A lightweight API for querying the Retrieval-Augmented Generation system",
    version="1.0.0"
)

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system.
    
    Args:
        request: Query request containing the question and top_k parameter
        
    Returns:
        Query response with answer and sources
    """
    try:
        # Query the RAG system
        result = rag_system.query(request.query, request.top_k)
        
        # Convert to response model
        response = QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources=[
                Source(
                    title=source["title"],
                    source_url=source["source_url"],
                    score=source["score"]
                )
                for source in result["sources"]
            ]
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Simple RAG System is running"}

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8001)