# Wikipedia Featured Article Integration

This extension adds functionality to fetch and integrate Wikipedia's featured articles into the RAG system.

## Features

1. **Featured Article Fetcher**: Fetches today's featured article from Wikipedia
2. **Historical Events**: Gets historical events that happened on today's date
3. **Page Descriptions**: Gets short descriptions of Wikipedia pages
4. **HTML Content**: Gets HTML versions of Wikipedia pages
5. **RAG Integration**: Seamlessly integrates featured articles into the RAG system
6. **Automated Updates**: Scripts to regularly update the RAG system with fresh content

## Files

- [`src/rag_system/data/featured_article_fetcher.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/src/rag_system/data/featured_article_fetcher.py) - Main module for fetching featured articles
- [`demo_featured_article.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/demo_featured_article.py) - Simple demo of the fetcher
- [`demo_wikimedia_apis.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/demo_wikimedia_apis.py) - Demo of various Wikimedia APIs
- [`example_featured_article_rag.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/example_featured_article_rag.py) - Example of integrating with RAG system
- [`update_rag_with_featured_article.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/update_rag_with_featured_article.py) - Script to update RAG with today's featured article
- [`query_featured_article.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/query_featured_article.py) - Script to query about the featured article

## Usage

### Simple Demo

```bash
python demo_featured_article.py
```

This will show today's featured article and historical events.

### Wikimedia APIs Demo

```bash
python demo_wikimedia_apis.py
```

This demonstrates various Wikimedia API integrations:
- Featured articles
- Page descriptions
- HTML content
- Historical events

### Update RAG System

```bash
python update_rag_with_featured_article.py
```

This will fetch today's featured article and add it to the RAG system.

### Query About Featured Article

```bash
python query_featured_article.py "What is the featured article about?"
```

## Integration with Existing Code

The `FeaturedArticleFetcher` extends the existing `WikipediaFetcher` and maintains compatibility with the existing RAG pipeline. You can use it as follows:

```python
from src.rag_system.data.featured_article_fetcher import FeaturedArticleFetcher

fetcher = FeaturedArticleFetcher()
featured_doc = fetcher.fetch_featured_article_as_document()

# featured_doc is formatted for direct use with the RAG system
```

## API Details

The integration uses the Wikimedia API endpoints:

### Featured Content
```
GET https://api.wikimedia.org/feed/v1/wikipedia/en/featured/YYYY/MM/DD
```

### Historical Events
```
GET https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/MM/DD
```

### Page Summaries (including descriptions)
```
GET https://en.wikipedia.org/api/rest_v1/page/summary/{title}
```

### Page HTML Content
```
GET https://en.wikipedia.org/api/rest_v1/page/html/{title}
```

These APIs are publicly accessible and don't require authentication.

## Methods Available

### `get_todays_featured_article()`
Fetches today's featured article from Wikipedia.

Returns a dictionary with:
- `title`: Article title
- `summary`: Article summary/excerpt
- `content`: Full article content (same as summary in this case)
- `url`: Link to the full article
- `page_id`: Wikipedia page ID
- `timestamp`: When the article was fetched

### `get_page_description(title)`
Gets a short description of a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page

Returns the description string or None if not found.

### `get_page_html(title)`
Gets the HTML content of a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page

Returns the HTML content as a string or None if not found.

### `get_on_this_day_events(limit=3)`
Gets historical events that happened on today's date.

Parameters:
- `limit`: Maximum number of events to return (default: 3)

Returns a list of event dictionaries or None if not found.

### `fetch_featured_article_as_document()`
Fetches today's featured article and formats it as a document for the RAG system.

Returns a dictionary formatted for the RAG pipeline with:
- `id`: Document ID
- `title`: Article title
- `source_url`: Link to the full article
- `text`: Article content