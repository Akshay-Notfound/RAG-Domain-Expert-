"""
Test script for Wikipedia integration with the RAG system.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_system.data.wikipedia_fetcher import WikipediaFetcher

def test_wikipedia_fetcher():
    """Test the Wikipedia fetcher functionality."""
    print("Testing Wikipedia Fetcher...")
    
    # Initialize the fetcher
    fetcher = WikipediaFetcher()
    
    # Test searching for articles
    print("\n1. Testing search functionality:")
    search_results = fetcher.search_wikipedia("Artificial Intelligence", 3)
    print(f"Found {len(search_results)} articles")
    
    for result in search_results:
        print(f"  - {result['title']}")
    
    # Test fetching full content
    print("\n2. Testing full content fetch:")
    if search_results:
        first_article = fetcher.fetch_article_content(search_results[0]['title'])
        if first_article:
            print(f"  Title: {first_article['title']}")
            print(f"  URL: {first_article['url']}")
            print(f"  Content length: {len(first_article['content'])} characters")
        else:
            print("  Failed to fetch article content")
    else:
        print("  No search results to fetch content from")
    
    # Test search and fetch combined
    print("\n3. Testing search and fetch combined:")
    articles = fetcher.search_and_fetch_articles("Machine Learning", 2)
    print(f"Successfully fetched {len(articles)} articles")
    
    for article in articles:
        print(f"  - {article['title']}: {article['source_url']}")

if __name__ == "__main__":
    test_wikipedia_fetcher()