"""
Data module for the RAG system.
Handles data ingestion, preprocessing, and chunking.
"""

from .document_processor import DocumentProcessor
from .wikipedia_fetcher import WikipediaFetcher
from .featured_article_fetcher import FeaturedArticleFetcher
from .wikipedia_api_fetcher import WikipediaApiFetcher