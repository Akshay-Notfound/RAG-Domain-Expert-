import datetime
import requests
import json

def get_todays_featured_article():
    """Get today's featured article from English Wikipedia"""
    today = datetime.datetime.now()
    date = today.strftime('%Y/%m/%d')
    
    # Public API endpoint for featured content (no auth required)
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{date}'
    
    # Headers without authentication for public access
    headers = {
        'User-Agent': 'RAG-System/1.0 (educational-purpose)'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        # Extract today's featured article (tfa = today's featured article)
        if 'tfa' in data:
            featured_article = data['tfa']
            title = featured_article.get('title', 'Unknown Title')
            extract = featured_article.get('extract', 'No extract available')
            page_url = featured_article.get('content_urls', {}).get('desktop', {}).get('page', '')
            
            print("=" * 60)
            print("TODAY'S FEATURED ARTICLE FROM WIKIPEDIA")
            print("=" * 60)
            print(f"Title: {title}")
            print(f"URL: {page_url}")
            print(f"\nSummary:\n{extract}")
            print("=" * 60)
            
            # Return the data for potential use in RAG system
            return {
                'title': title,
                'summary': extract,
                'url': page_url
            }
        else:
            print("No featured article found for today.")
            print("Available keys in response:", list(data.keys()))
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_on_this_day_events():
    """Get historical events that happened on today's date"""
    today = datetime.datetime.now()
    date = today.strftime('%m/%d')  # Month/Day format for historical events
    
    # Public API endpoint for historical events
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{date}'
    
    headers = {
        'User-Agent': 'RAG-System/1.0 (educational-purpose)'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print("\n" + "=" * 60)
        print("HISTORICAL EVENTS THAT HAPPENED TODAY")
        print("=" * 60)
        
        # Extract events
        if 'events' in data and len(data['events']) > 0:
            # Show the most recent 3 events
            for i, event in enumerate(data['events'][:3]):
                year = event.get('year', 'Unknown year')
                text = event.get('text', 'No description')
                print(f"{year}: {text}")
                
            print("=" * 60)
            return data['events'][:3]  # Return first 3 events
        else:
            print("No historical events found for today.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    # Get today's featured article
    featured = get_todays_featured_article()
    
    # Get historical events
    events = get_on_this_day_events()