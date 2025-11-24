"""
Demo script showing how to use various Wikimedia APIs with the RAG system.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher


def main():
    """Demonstrate using various Wikimedia APIs."""
    print("Demonstrating Wikimedia API integrations")
    print("=" * 50)
    
    # Initialize the fetcher
    fetcher = FeaturedArticleFetcher()
    
    # 1. Get today's featured article (already implemented)
    print("1. Today's Featured Article:")
    article = fetcher.get_todays_featured_article()
    if article:
        print(f"   Title: {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Summary: {article['summary'][:100]}...")
    else:
        print("   Could not fetch featured article")
    
    print("\n" + "=" * 50)
    
    # 2. Get a short description of a page
    print("2. Page Description (for 'Python (programming_language)'):")
    description = fetcher.get_page_description("Python (programming_language)")
    if description:
        print(f"   Description: {description}")
    else:
        print("   Could not fetch description")
    
    print("\n" + "=" * 50)
    
    # 3. Get HTML content of a page
    print("3. HTML Content (for 'Python (programming_language)'):")
    html_content = fetcher.get_page_html("Python (programming_language)")
    if html_content:
        # Show the length and first part of the content
        print(f"   HTML Length: {len(html_content)} characters")
        # Clean up the HTML for display
        clean_text = html_content.replace('\n', ' ').replace('\r', ' ')
        print(f"   HTML Preview: {clean_text[:200]}...")
    else:
        print("   Could not fetch HTML content")
    
    print("\n" + "=" * 50)
    
    # 4. Get historical events
    print("4. Historical Events (today in history):")
    events = fetcher.get_on_this_day_events(limit=2)
    if events:
        for i, event in enumerate(events, 1):
            print(f"   {i}. {event['year']}: {event['text']}")
    else:
        print("   Could not fetch historical events")


if __name__ == "__main__":
    main()