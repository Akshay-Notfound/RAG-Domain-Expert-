"""
Featured Article Fetcher for the RAG system.
Extends WikipediaFetcher to include featured article functionality.
"""

import datetime
import requests
import json
from typing import Dict, Any, Optional, List
from .wikipedia_fetcher import WikipediaFetcher


class FeaturedArticleFetcher(WikipediaFetcher):
    """Extended Wikipedia fetcher that can fetch featured articles."""
    
    def __init__(self):
        """Initialize the featured article fetcher."""
        super().__init__()
        self.featured_base_url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/"
        self.onthisday_base_url = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/"
        self.core_base_url = "https://en.wikipedia.org/api/rest_v1/page/"
    
    def get_todays_featured_article(self) -> Optional[Dict[str, Any]]:
        """
        Get today's featured article from English Wikipedia.
        
        Returns:
            Dictionary with featured article data or None if not found
        """
        today = datetime.datetime.now()
        date = today.strftime('%Y/%m/%d')
        
        # API endpoint for featured content
        url = f'{self.featured_base_url}{date}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Extract today's featured article (tfa = today's featured article)
            if 'tfa' in data:
                featured_article = data['tfa']
                title = featured_article.get('title', 'Unknown Title')
                extract = featured_article.get('extract', 'No extract available')
                page_url = featured_article.get('content_urls', {}).get('desktop', {}).get('page', '')
                
                return {
                    'title': title,
                    'summary': extract,
                    'content': extract,  # For compatibility with existing RAG pipeline
                    'url': page_url,
                    'page_id': featured_article.get('pageid', ''),
                    'timestamp': today.isoformat()
                }
            else:
                print("No featured article found for today.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching featured article: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_page_description(self, title: str) -> Optional[str]:
        """
        Get a short description of a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            Short description of the page or None if not found
        """
        # Replace spaces with underscores for URL
        formatted_title = title.replace(' ', '_')
        url = f'{self.core_base_url}summary/{formatted_title}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('description', None)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page description: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_page_html(self, title: str) -> Optional[str]:
        """
        Get the HTML version of a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            HTML content of the page or None if not found
        """
        # Replace spaces with underscores for URL
        formatted_title = title.replace(' ', '_')
        # Different URL structure for HTML content
        url = f"https://en.wikipedia.org/api/rest_v1/page/html/{formatted_title}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page HTML: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_on_this_day_events(self, limit: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Get historical events that happened on today's date.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of historical events or None if error occurs
        """
        today = datetime.datetime.now()
        date = today.strftime('%m/%d')  # Month/Day format for historical events
        
        # API endpoint for historical events
        url = f'{self.onthisday_base_url}{date}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Extract events
            if 'events' in data and len(data['events']) > 0:
                events = []
                for i, event in enumerate(data['events'][:limit]):
                    events.append({
                        'year': event.get('year', 'Unknown year'),
                        'text': event.get('text', 'No description'),
                        'pages': event.get('pages', [])
                    })
                return events
            else:
                print("No historical events found for today.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def fetch_featured_article_as_document(self) -> Optional[Dict[str, Any]]:
        """
        Fetch today's featured article and format it as a document for the RAG system.
        
        Returns:
            Formatted document dictionary for RAG or None if not found
        """
        article = self.get_todays_featured_article()
        if article:
            return self.format_document_for_rag(article)
        return None


# Example usage
if __name__ == "__main__":
    fetcher = FeaturedArticleFetcher()
    
    # Get today's featured article
    featured_doc = fetcher.fetch_featured_article_as_document()
    
    if featured_doc:
        print("Today's Featured Article:")
        print(f"Title: {featured_doc['title']}")
        print(f"URL: {featured_doc['source_url']}")
        print(f"Text preview: {featured_doc['text'][:200]}...")
        
        # Get a short description of the featured article
        description = fetcher.get_page_description(featured_doc['title'])
        if description:
            print(f"\nDescription: {description}")
    else:
        print("Could not fetch today's featured article.")