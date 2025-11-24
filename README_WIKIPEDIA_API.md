# Wikipedia-API Library Integration

This extension adds comprehensive Wikipedia data fetching capabilities using the [wikipedia-api](https://github.com/martin-majlis/Wikipedia-API) library.

## Features

1. **Full Page Content**: Retrieve complete Wikipedia pages with all sections
2. **Structured Data**: Access to sections, links, categories in organized format
3. **Detailed Information**: Get specific sections, links, and categories
4. **RAG Integration**: Seamlessly integrate Wikipedia content into the RAG system
5. **Multiple Formats**: Support for both WIKI and HTML content formats

## Files

- [`src/rag_system/data/wikipedia_api_fetcher.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/src/rag_system/data/wikipedia_api_fetcher.py) - Main module for fetching Wikipedia content using the library
- [`demo_wikipedia_api.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/demo_wikipedia_api.py) - Demo of the Wikipedia-API library
- [`example_wikipedia_api_rag.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/example_wikipedia_api_rag.py) - Example of integrating with RAG system
- [`compare_wikipedia_fetchers.py`](file:///d:/Projects%20for%20Final%20Year%20testing/RAG/compare_wikipedia_fetchers.py) - Comparison of different Wikipedia fetchers

## Installation

The wikipedia-api library is already included in your project dependencies. If you need to install it separately:

```bash
pip install wikipedia-api
```

## Usage

### Simple Demo

```bash
python demo_wikipedia_api.py
```

This will show various capabilities of the Wikipedia-API library.

### Compare Fetchers

```bash
python compare_wikipedia_fetchers.py
```

This compares the different Wikipedia fetchers available in the system.

### Integrate with RAG System

```bash
python example_wikipedia_api_rag.py
```

This demonstrates how to integrate Wikipedia content with the RAG system.

## Integration with Existing Code

The `WikipediaApiFetcher` provides a clean interface for fetching Wikipedia content. You can use it as follows:

```python
from src.rag_system.data.wikipedia_api_fetcher import WikipediaApiFetcher

fetcher = WikipediaApiFetcher()
document = fetcher.format_page_as_document("Python (programming language)")

# document is formatted for direct use with the RAG system
```

## Methods Available

### `get_page(title)`
Get a Wikipedia page by title.

Parameters:
- `title`: Title of the Wikipedia page

Returns a WikipediaPage object or None if page doesn't exist.

### `get_page_summary(title, chars=500)`
Get the summary of a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page
- `chars`: Number of characters to return (default: 500)

Returns the summary text or None if page doesn't exist.

### `get_full_text(title)`
Get the full text of a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page

Returns the full text of the page or None if page doesn't exist.

### `get_sections(title)`
Get all sections of a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page

Returns a list of sections with titles and text or None if page doesn't exist.

### `get_section_by_title(page_title, section_title)`
Get a specific section by title from a Wikipedia page.

Parameters:
- `page_title`: Title of the Wikipedia page
- `section_title`: Title of the section to retrieve

Returns a section dictionary with title and text or None if not found.

### `get_links(title, limit=50)`
Get links from a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page
- `limit`: Maximum number of links to return (default: 50)

Returns a list of linked page titles or None if page doesn't exist.

### `get_categories(title, limit=50)`
Get categories for a Wikipedia page.

Parameters:
- `title`: Title of the Wikipedia page
- `limit`: Maximum number of categories to return (default: 50)

Returns a list of category names or None if page doesn't exist.

### `format_page_as_document(title)`
Format a Wikipedia page as a document for the RAG system.

Parameters:
- `title`: Title of the Wikipedia page

Returns a formatted document dictionary for RAG or None if page doesn't exist.

## Example Usage

```python
from src.rag_system.data.wikipedia_api_fetcher import WikipediaApiFetcher

# Initialize the fetcher
fetcher = WikipediaApiFetcher()

# Get information about a topic
title = "Machine learning"
page = fetcher.get_page(title)

if page:
    # Get the summary
    summary = fetcher.get_page_summary(title, 300)
    print(f"Summary: {summary}")
    
    # Get all sections
    sections = fetcher.get_sections(title)
    print(f"Number of sections: {len(sections)}")
    
    # Get a specific section
    history_section = fetcher.get_section_by_title(title, "History")
    if history_section:
        print(f"History: {history_section['text'][:200]}...")
    
    # Format for RAG system
    document = fetcher.format_page_as_document(title)
    print(f"Document ID: {document['id']}")
    print(f"Text length: {len(document['text'])} characters")
```

## Advantages Over Other Fetchers

1. **More Comprehensive**: Access to full page structure including sections, links, and categories
2. **Better Organization**: Structured data that's easier to work with
3. **Richer Information**: More detailed content than summary-only approaches
4. **Reliable**: Well-maintained library with good documentation
5. **Flexible**: Support for different content formats (WIKI/HTML)

## Use Cases

1. **Educational Applications**: Get detailed information about topics for learning
2. **Research Tools**: Access comprehensive Wikipedia content for analysis
3. **Content Enrichment**: Add detailed Wikipedia information to your knowledge base
4. **Question Answering**: Use detailed section information to answer specific questions
5. **Link Analysis**: Analyze connections between Wikipedia pages