"""
Comparison script showing the differences between the two Wikipedia fetchers.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rag_system.data.wikipedia_fetcher import WikipediaFetcher
from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher
from src.rag_system.data.wikipedia_api_fetcher import WikipediaApiFetcher


def main():
    """Compare the different Wikipedia fetchers."""
    print("Comparing Wikipedia Fetchers")
    print("=" * 50)
    
    # Initialize all fetchers
    traditional_fetcher = WikipediaFetcher()
    featured_fetcher = FeaturedArticleFetcher()
    api_fetcher = WikipediaApiFetcher()
    
    # 1. Traditional Wikipedia Fetcher
    print("1. Traditional Wikipedia Fetcher")
    print("   - Uses Wikipedia's REST API")
    print("   - Good for searching and fetching articles by title")
    print("   - Returns structured data")
    
    search_results = traditional_fetcher.search_wikipedia("Python programming", 2)
    if search_results:
        print(f"   - Example search results: {len(search_results)} found")
        for result in search_results:
            print(f"     * {result['title']}")
    
    # 2. Featured Article Fetcher
    print("\n2. Featured Article Fetcher")
    print("   - Extends traditional fetcher")
    print("   - Can fetch today's featured article")
    print("   - Can get historical events")
    print("   - Can get page descriptions and HTML")
    
    featured_article = featured_fetcher.get_todays_featured_article()
    if featured_article:
        print(f"   - Today's featured article: {featured_article['title']}")
    
    # 3. Wikipedia-API Fetcher
    print("\n3. Wikipedia-API Fetcher")
    print("   - Uses the wikipedia-api library")
    print("   - More comprehensive page information")
    print("   - Access to sections, links, categories")
    print("   - Better structured data")
    
    api_page = api_fetcher.get_page("Python (programming language)")
    if api_page:
        print(f"   - Example page: {api_page.title}")
        sections = api_fetcher.get_sections("Python (programming language)")
        if sections:
            print(f"   - Number of sections: {len(sections)}")
        links = api_fetcher.get_links("Python (programming language)", 5)
        if links:
            print(f"   - Sample links: {', '.join(links[:3])}")
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("  - Traditional Fetcher: Best for general searches")
    print("  - Featured Fetcher: Best for daily updates and special content")
    print("  - Wikipedia-API Fetcher: Best for detailed page analysis")


if __name__ == "__main__":
    main()