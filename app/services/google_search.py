import requests
import time

SERPER_API_KEY = "3dd5a20770d46cc60635bd3fbf4194ce41014ea9"

def search_instagram_posts(hashtag: str, location: str, limit: int = 300):
    """
    Search for Instagram posts with a given hashtag.
    Note: Due to API limitations, actual results may be fewer than requested.
    """
    query = f'site:instagram.com/p "#{hashtag}" "{location}"'
    print(f"Searching for Instagram posts with hashtag: {query}")
    all_links = set()
    page = 1
    results_per_page = 10  # Serper typically returns 10 results per page
    max_pages = min((limit // results_per_page) + 1, 10)  # Limit to 10 pages max
    
    for page_num in range(max_pages):
        payload = {
            "q": query,
            "num": results_per_page,
            "page": page_num + 1  # Pages are 1-indexed
        }
        
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            r.raise_for_status()
            data = r.json()
            
            # Extract links from organic results
            organic_results = data.get("organic", [])
            
            if not organic_results:
                print(f"No more results found at page {page_num + 1}")
                break
            
            for item in organic_results:
                link = item.get("link")
                if link and "/p/" in link:
                    all_links.add(link)
            
            print(f"Page {page_num + 1}: Found {len(organic_results)} results, total unique links: {len(all_links)}")
            
            # Stop if we've reached our limit
            if len(all_links) >= limit:
                break
            
            # Be respectful with API rate limits
            if page_num < max_pages - 1:
                time.sleep(1)  # Wait 1 second between requests
                
        except requests.exceptions.RequestException as e:
            print(f"Error on page {page_num + 1}: {e}")
            break
    
    return list(all_links)[:limit]