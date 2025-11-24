"""
Wikipedia-API Fetcher for the RAG system.
Uses the wikipedia-api library to fetch content from Wikipedia.
"""

import wikipediaapi
from typing import List, Dict, Any, Optional
from .document_processor import DocumentProcessor


class WikipediaApiFetcher:
    """Fetch content from Wikipedia using the wikipedia-api library."""
    
    def __init__(self, user_agent: str = "RAG-System/1.0 (educational-project)"):
        """
        Initialize the Wikipedia API fetcher.
        
        Args:
            user_agent: User agent string to identify the application
        """
        self.user_agent = user_agent
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
    
    def get_page(self, title: str) -> Optional[wikipediaapi.WikipediaPage]:
        """
        Get a Wikipedia page by title.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            WikipediaPage object or None if page doesn't exist
        """
        page = self.wiki_wiki.page(title)
        return page if page.exists() else None
    
    def get_page_summary(self, title: str, chars: int = 500) -> Optional[str]:
        """
        Get the summary of a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            chars: Number of characters to return (default: 500)
            
        Returns:
            Summary text or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            return page.summary[:chars]
        return None
    
    def get_full_text(self, title: str) -> Optional[str]:
        """
        Get the full text of a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            Full text of the page or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            return page.text
        return None
    
    def get_sections(self, title: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get all sections of a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            List of sections with titles and text or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            sections = []
            self._extract_sections(page.sections, sections)
            return sections
        return None
    
    def _extract_sections(self, page_sections, sections_list: List[Dict[str, Any]], level: int = 0):
        """
        Recursively extract sections from a Wikipedia page.
        
        Args:
            page_sections: Sections from a Wikipedia page
            sections_list: List to append sections to
            level: Current section level (for hierarchy tracking)
        """
        for section in page_sections:
            sections_list.append({
                'title': section.title,
                'text': section.text,
                'level': level
            })
            # Recursively extract subsections
            if section.sections:
                self._extract_sections(section.sections, sections_list, level + 1)
    
    def get_section_by_title(self, page_title: str, section_title: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific section by title from a Wikipedia page.
        
        Args:
            page_title: Title of the Wikipedia page
            section_title: Title of the section to retrieve
            
        Returns:
            Section dictionary with title and text or None if not found
        """
        page = self.get_page(page_title)
        if page:
            section = page.section_by_title(section_title)
            if section:
                return {
                    'title': section.title,
                    'text': section.text
                }
        return None
    
    def get_links(self, title: str, limit: int = 50) -> Optional[List[str]]:
        """
        Get links from a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            limit: Maximum number of links to return (default: 50)
            
        Returns:
            List of linked page titles or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            links = list(page.links.keys())[:limit]
            return links
        return None
    
    def get_categories(self, title: str, limit: int = 50) -> Optional[List[str]]:
        """
        Get categories for a Wikipedia page.
        
        Args:
            title: Title of the Wikipedia page
            limit: Maximum number of categories to return (default: 50)
            
        Returns:
            List of category names or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            categories = list(page.categories.keys())[:limit]
            return categories
        return None
    
    def search_pages(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for Wikipedia pages (placeholder - wikipedia-api doesn't have direct search).
        This is a simplified implementation that tries to get pages with similar names.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of page information dictionaries
        """
        # This is a simplified approach since wikipedia-api doesn't have a direct search function
        # We'll try to get the page directly and see if it exists
        page = self.get_page(query)
        if page:
            return [{
                'title': page.title,
                'summary': page.summary[:200] if page.summary else '',
                'url': page.fullurl
            }]
        else:
            # If direct page doesn't exist, try with underscores instead of spaces
            page_with_underscores = self.get_page(query.replace(' ', '_'))
            if page_with_underscores:
                return [{
                    'title': page_with_underscores.title,
                    'summary': page_with_underscores.summary[:200] if page_with_underscores.summary else '',
                    'url': page_with_underscores.fullurl
                }]
        
        # Return empty list if no pages found
        return []
    
    def format_page_as_document(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Format a Wikipedia page as a document for the RAG system.
        
        Args:
            title: Title of the Wikipedia page
            
        Returns:
            Formatted document dictionary for RAG or None if page doesn't exist
        """
        page = self.get_page(title)
        if page:
            return {
                'id': f"wikipedia_api_{title.replace(' ', '_')}",
                'title': page.title,
                'source_url': page.fullurl,
                'text': page.text
            }
        return None


# Example usage
if __name__ == "__main__":
    fetcher = WikipediaApiFetcher()
    
    # Get information about Python programming language
    title = "Python (programming language)"
    
    print(f"Fetching information about: {title}")
    print("=" * 50)
    
    # Get page summary
    summary = fetcher.get_page_summary(title)
    if summary:
        print(f"Summary: {summary}")
    
    print("\n" + "=" * 50)
    
    # Get full text
    print("Full text length:", len(fetcher.get_full_text(title) or ""))
    
    # Get sections
    sections = fetcher.get_sections(title)
    if sections:
        print(f"\nFirst 3 sections:")
        for i, section in enumerate(sections[:3]):
            print(f"  {i+1}. {section['title']}")
    
    # Get specific section
    history_section = fetcher.get_section_by_title(title, "History")
    if history_section:
        print(f"\nHistory section preview: {history_section['text'][:100]}...")
    
    # Get links
    links = fetcher.get_links(title, 5)
    if links:
        print(f"\nFirst 5 links: {links}")
    
    # Format as document for RAG
    document = fetcher.format_page_as_document(title)
    if document:
        print(f"\nFormatted as RAG document:")
        print(f"  ID: {document['id']}")
        print(f"  Title: {document['title']}")
        print(f"  URL: {document['source_url']}")
        print(f"  Text length: {len(document['text'])} characters")