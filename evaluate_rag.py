"""
Evaluation script for the RAG system.
This script evaluates the RAG system using sample questions and expected answers.
"""

import os
import sys
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.rag_pipeline import RAGSystem


def evaluate_rag_system():
    """Evaluate the RAG system with sample questions."""
    
    print("Evaluating RAG System...")
    
    # Create RAG system instance
    rag_system = RAGSystem()
    
    # Sample evaluation data
    evaluation_data = [
        {
            "question": "Who led the Salt Satyagraha in 1930?",
            "expected_keywords": ["Gandhi", "Mahatma", "Salt March", "Satyagraha"]
        },
        {
            "question": "What was the purpose of the Salt March?",
            "expected_keywords": ["protest", "salt tax", "British", "civil disobedience"]
        },
        {
            "question": "When did the Salt March begin and end?",
            "expected_keywords": ["1930", "March 12", "April 5"]
        }
    ]
    
    # Initialize with sample documents (same as in init_rag.py)
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
        }
    ]
    
    # Add documents and build index
    print("Setting up evaluation data...")
    rag_system.add_documents(sample_documents)
    rag_system.build_index()
    
    # Evaluate each question
    correct_answers = 0
    total_questions = len(evaluation_data)
    
    print(f"\nEvaluating {total_questions} questions...\n")
    
    for i, eval_item in enumerate(evaluation_data, 1):
        question = eval_item["question"]
        expected_keywords = eval_item["expected_keywords"]
        
        print(f"{i}. Question: {question}")
        
        # Get answer from RAG system
        result = rag_system.query(question)
        answer = result["answer"].lower()
        
        print(f"   Answer: {result['answer']}")
        
        # Check if expected keywords are in the answer
        found_keywords = [keyword for keyword in expected_keywords if keyword.lower() in answer]
        missing_keywords = [keyword for keyword in expected_keywords if keyword.lower() not in answer]
        
        if len(found_keywords) > 0:
            correct_answers += 1
            print(f"   ✓ Found keywords: {', '.join(found_keywords)}")
            if missing_keywords:
                print(f"   ⚠ Missing keywords: {', '.join(missing_keywords)}")
        else:
            print(f"   ✗ No expected keywords found. Missing: {', '.join(missing_keywords)}")
        
        print()
    
    # Calculate accuracy
    accuracy = (correct_answers / total_questions) * 100
    print(f"Evaluation Results:")
    print(f"Correctly answered: {correct_answers}/{total_questions} ({accuracy:.1f}%)")
    
    if accuracy >= 80:
        print("✓ System performance is good!")
    elif accuracy >= 60:
        print("⚠ System performance is acceptable but could be improved.")
    else:
        print("✗ System performance needs improvement.")
    
    return accuracy


if __name__ == "__main__":
    evaluate_rag_system()