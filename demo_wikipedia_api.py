"""
Demo script showing how to use the Wikipedia-API library with the RAG system.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.wikipedia_api_fetcher import WikipediaApiFetcher


def main():
    """Demonstrate using the Wikipedia-API library."""
    print("Demonstrating Wikipedia-API library integration")
    print("=" * 50)
    
    # Initialize the fetcher
    fetcher = WikipediaApiFetcher()
    
    # Example 1: Get information about Python programming language
    title = "Python (programming language)"
    print(f"1. Information about: {title}")
    
    # Get page summary
    summary = fetcher.get_page_summary(title, 300)
    if summary:
        print(f"   Summary: {summary}")
    
    # Get page URL
    page = fetcher.get_page(title)
    if page:
        print(f"   URL: {page.fullurl}")
    
    # Get sections
    sections = fetcher.get_sections(title)
    if sections:
        print(f"   Number of sections: {len(sections)}")
        print("   First 3 sections:")
        for i, section in enumerate(sections[:3]):
            print(f"     {i+1}. {section['title']}")
    
    print("\n" + "=" * 50)
    
    # Example 2: Get a specific section
    print("2. History section of Python:")
    history_section = fetcher.get_section_by_title(title, "History")
    if history_section:
        # Show first 200 characters of the history section
        print(f"   Preview: {history_section['text'][:200]}...")
    else:
        print("   History section not found")
    
    print("\n" + "=" * 50)
    
    # Example 3: Get links from the page
    print("3. First 10 links from Python page:")
    links = fetcher.get_links(title, 10)
    if links:
        for i, link in enumerate(links, 1):
            print(f"   {i}. {link}")
    else:
        print("   No links found")
    
    print("\n" + "=" * 50)
    
    # Example 4: Get categories
    print("4. First 5 categories of Python page:")
    categories = fetcher.get_categories(title, 5)
    if categories:
        for i, category in enumerate(categories, 1):
            print(f"   {i}. {category}")
    else:
        print("   No categories found")
    
    print("\n" + "=" * 50)
    
    # Example 5: Format as RAG document
    print("5. Formatted as RAG document:")
    document = fetcher.format_page_as_document(title)
    if document:
        print(f"   ID: {document['id']}")
        print(f"   Title: {document['title']}")
        print(f"   URL: {document['source_url']}")
        print(f"   Text length: {len(document['text'])} characters")
    else:
        print("   Could not format as document")


if __name__ == "__main__":
    main()