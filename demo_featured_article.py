"""
Demo script showing how to fetch and use Wikipedia's featured article.
"""

from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher


def main():
    """Demonstrate fetching and displaying Wikipedia's featured article."""
    print("Fetching today's featured article from Wikipedia...")
    print("=" * 60)
    
    # Initialize the featured article fetcher
    fetcher = FeaturedArticleFetcher()
    
    # Fetch today's featured article
    article = fetcher.get_todays_featured_article()
    
    if not article:
        print("Could not fetch today's featured article.")
        return
    
    # Display the article information
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print("\nSummary:")
    print(article['summary'])
    print("=" * 60)
    
    # Show how this can be used as a document in the RAG system
    print("\nFormatted as RAG document:")
    doc = fetcher.format_document_for_rag(article)
    print(f"ID: {doc['id']}")
    print(f"Title: {doc['title']}")
    print(f"Source URL: {doc['source_url']}")
    print(f"Text preview: {doc['text'][:100]}...")
    print("=" * 60)
    
    # Fetch historical events
    print("\nHistorical events that happened today:")
    events = fetcher.get_on_this_day_events(limit=3)
    
    if events:
        for i, event in enumerate(events, 1):
            print(f"{i}. {event['year']}: {event['text']}")
    else:
        print("No historical events found.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()