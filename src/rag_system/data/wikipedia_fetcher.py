"""
Wikipedia Fetcher for the RAG system.
Handles fetching content from Wikipedia and preparing it for the RAG pipeline.
"""

import requests
import re
import json
import os
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup


class WikipediaFetcher:
    """Fetch content from Wikipedia and prepare it for the RAG system."""
    
    def __init__(self):
        """Initialize the Wikipedia fetcher."""
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        self.content_url = "https://en.wikipedia.org/w/api.php"
        # Set a user agent to avoid blocking
        self.headers = {
            'User-Agent': 'RAG-System/1.0 (Educational Research Project)'
        }
        self._load_credentials()

    def _load_credentials(self):
        """Load API credentials from config.json and authenticate if present."""
        try:
            # Find config.json relative to this file
            # src/rag_system/data/wikipedia_fetcher.py -> ../../../config.json
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                wiki_config = config.get('wikipedia_api', {})
                client_id = wiki_config.get('client_id')
                client_secret = wiki_config.get('client_secret')
                
                if client_id and client_secret:
                    print("Found Wikipedia API credentials, attempting to authenticate...")
                    self._authenticate(client_id, client_secret)
        except Exception as e:
            print(f"Error loading credentials: {e}")

    def _authenticate(self, client_id: str, client_secret: str):
        """
        Authenticate with Wikimedia OAuth to get an access token.
        
        Args:
            client_id: OAuth Client ID
            client_secret: OAuth Client Secret
        """
        auth_url = "https://meta.wikimedia.org/w/rest.php/oauth2/access_token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        try:
            response = requests.post(auth_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                if access_token:
                    self.headers['Authorization'] = f"Bearer {access_token}"
                    print("Successfully authenticated with Wikipedia API.")
                else:
                    print("Authentication failed: No access token in response.")
            else:
                print(f"Authentication failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Authentication error: {e}")
    
    def search_wikipedia(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Wikipedia for articles matching the query.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of article summaries
        """
        search_params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit
        }
        
        try:
            response = requests.get(self.content_url, params=search_params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('query', {}).get('search', []):
                results.append({
                    'title': item.get('title', ''),
                    'snippet': self._clean_html(item.get('snippet', '')),
                    'pageid': item.get('pageid', '')
                })
            
            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    
    def fetch_article_content(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full content of a Wikipedia article.
        
        Args:
            title: Title of the Wikipedia article
            
        Returns:
            Dictionary with article content or None if not found
        """
        # First get basic info from summary API
        try:
            summary_response = requests.get(f"{self.base_url}{title}", headers=self.headers)
            summary_response.raise_for_status()
            summary_data = summary_response.json()
        except Exception as e:
            print(f"Error fetching summary for {title}: {e}")
            return None
        
        # Then get full content
        content_params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'explaintext': True,
            'exsectionformat': 'wiki'
        }
        
        try:
            content_response = requests.get(self.content_url, params=content_params, headers=self.headers)
            content_response.raise_for_status()
            content_data = content_response.json()
            
            pages = content_data.get('query', {}).get('pages', {})
            page = list(pages.values())[0] if pages else {}
            
            if 'missing' in page:
                return None
                
            return {
                'title': page.get('title', title),
                'summary': summary_data.get('extract', ''),
                'content': page.get('extract', ''),
                'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'page_id': page.get('pageid', '')
            }
        except Exception as e:
            print(f"Error fetching content for {title}: {e}")
            return None
    
    def format_document_for_rag(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a Wikipedia article for the RAG system.
        
        Args:
            article: Wikipedia article data
            
        Returns:
            Formatted document dictionary for RAG
        """
        return {
            'id': f"wikipedia_{article.get('page_id', '')}",
            'title': article.get('title', ''),
            'source_url': article.get('url', ''),
            'text': article.get('content', article.get('summary', ''))
        }
    
    def search_and_fetch_articles(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search Wikipedia and fetch full content for top results.
        
        Args:
            query: Search query
            limit: Maximum number of articles to fetch
            
        Returns:
            List of formatted documents for RAG
        """
        # Search for articles
        search_results = self.search_wikipedia(query, limit)
        
        # Fetch full content for each article
        documents = []
        for result in search_results:
            article = self.fetch_article_content(result['title'])
            if article:
                document = self.format_document_for_rag(article)
                documents.append(document)
        
        return documents
    
    def _clean_html(self, text: str) -> str:
        """
        Clean HTML tags from text.
        
        Args:
            text: Text with HTML tags
            
        Returns:
            Cleaned text
        """
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        
        # Decode HTML entities
        text = BeautifulSoup(text, "html.parser").get_text()
        
        return text


# Example usage
if __name__ == "__main__":
    fetcher = WikipediaFetcher()
    
    # Search for articles
    results = fetcher.search_and_fetch_articles("Artificial Intelligence", 2)
    
    print(f"Found {len(results)} articles:")
    for doc in results:
        print(f"- {doc['title']}: {doc['source_url']}")