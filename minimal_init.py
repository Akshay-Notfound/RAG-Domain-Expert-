"""
Minimal initialization script for the RAG system.
This script sets up the RAG system with minimal dependencies.
"""

import os
import sys
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Create data and indexes directories if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("indexes", exist_ok=True)

# Create a simple chunks file with sample data
sample_chunks = [
    {
        "id": "doc_1_0",
        "text": "Mahatma Gandhi led the Salt Satyagraha in 1930, walking from Sabarmati Ashram to Dandi to protest the British salt tax. The 24-day march covered 240 miles and became a pivotal act of non-violent civil disobedience. This movement mobilized mass participation across India and highlighted the injustice of colonial laws. The Salt March began on March 12, 1930, and ended on April 5, 1930, when Gandhi picked up a handful of salt from the Arabian Sea, symbolically violating the Salt Act.",
        "title": "Gandhi's Salt March",
        "source_url": "https://example.com/history/india/salt-march",
        "start_pos": 0,
        "end_pos": 500
    },
    {
        "id": "doc_2_0",
        "text": "The Salt Act prohibited Indians from collecting or selling salt, a basic necessity. This law was a key source of revenue for the British colonial government and was deeply resented by the Indian population. The tax on salt was seen as a symbol of British exploitation. The Act gave the British government a monopoly on the production and sale of salt, forcing Indians to buy expensive, imported salt instead of making their own.",
        "title": "The Salt Act of 1882",
        "source_url": "https://example.com/history/india/salt-act",
        "start_pos": 0,
        "end_pos": 500
    }
]

# Save chunks to file
chunks_file = "data/chunks.jsonl"
with open(chunks_file, 'w', encoding='utf-8') as f:
    for chunk in sample_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

# Create a simple metadata file
metadata = [
    {
        "id": "doc_1_0",
        "document_id": "doc_1",
        "title": "Gandhi's Salt March",
        "source_url": "https://example.com/history/india/salt-march"
    },
    {
        "id": "doc_2_0",
        "document_id": "doc_2",
        "title": "The Salt Act of 1882",
        "source_url": "https://example.com/history/india/salt-act"
    }
]

metadata_file = "data/metadata.json"
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("RAG system initialized with minimal data!")
print(f"Created {len(sample_chunks)} chunks")
print(f"Chunks file: {chunks_file}")
print(f"Metadata file: {metadata_file}")
print("\nYou can now start the API server with:")
print("  cd src/rag_system/api")
print("  python main.py")