"""
Initialization script for the RAG system.
This script helps set up the RAG system with sample data.
"""

import os
import sys
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def initialize_with_sample_data():
    """Initialize the RAG system with sample historical data."""
    
    # Create RAG system instance
    rag_system = RAGSystem()
    
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
        },
        {
            "id": "gandhi_1",
            "title": "Mahatma Gandhi",
            "source_url": "https://example.com/history/india/gandhi",
            "text": "Mohandas Karamchand Gandhi, known as Mahatma Gandhi, was an Indian lawyer and political ethicist who employed nonviolent resistance to lead the successful campaign for India's independence from British rule. Born in 1869 in Gujarat, he studied law in London and later practiced in South Africa before returning to India in 1915. Gandhi's philosophy of nonviolent resistance, or satyagraha, inspired movements for civil rights and freedom across the world."
        }
    ]
    
    print("Adding sample documents to the RAG system...")
    rag_system.add_documents(sample_documents)
    
    print("Building index...")
    rag_system.build_index()
    
    print("RAG system initialized with sample data!")
    print("\nYou can now start the API server with:")
    print("  cd src/rag_system")
    print("  python api/main.py")
    print("\nOr use Docker:")
    print("  docker-compose up --build")
    
    # Test a sample query
    print("\nTesting with a sample query...")
    result = rag_system.query("Who led the Salt Satyagraha in 1930 and why was it important?")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print("Sources:")
    for source in result['sources']:
        print(f"  - {source['title']} ({source['source_url']})")


if __name__ == "__main__":
    initialize_with_sample_data()