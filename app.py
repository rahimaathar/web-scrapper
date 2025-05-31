"""
A simple but practical web scraper to grab headings from websites.
I built this to help with content analysis and SEO research.

Usage:
1. Set your target URL
2. Choose what heading tags to scrape (h1, h2, etc.)
3. Get results in your terminal or save to files

Pro tips:
- Be nice and add delays between requests
- Some sites block scrapers - if it fails, try changing the user agent
- Check robots.txt first to see if scraping is allowed
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
import json

# Let's make this look like a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

def scrape_site(url, heading_type='h2', pause=2, save_files=True):
    """
    Main scraping function - does the heavy lifting
    
    Args:
        url: Website URL to scrape
        heading_type: Which HTML headings to grab (h1, h2, etc.)
        pause: Seconds to wait between requests (be polite!)
        save_files: Whether to save CSV/JSON files automatically
    
    Returns:
        List of heading dictionaries with text and metadata
    """
    print(f"\nStarting scrape of {url} for <{heading_type}> tags...")
    
    try:
        # Be a good internet citizen - don't hammer servers
        time.sleep(pause)
        
        print("Making request...")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Crash if request fails
        
        # Some sites return non-HTML for errors
        if 'text/html' not in response.headers.get('Content-Type', ''):
            print("Oops! Didn't get HTML back - maybe a redirect or error page?")
            return []
        
        print("Parsing page content...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all headings of our specified type
        headings = soup.find_all(heading_type)
        if not headings:
            print(f"No <{heading_type}> tags found on this page")
            return []
        
        # Build our results
        results = []
        for i, heading in enumerate(headings, 1):
            heading_text = heading.get_text().strip()
            results.append({
                'order': i,
                'type': heading_type,
                'text': heading_text,
                'url': url
            })
            print(f"  {i}. {heading_text[:60]}{'...' if len(heading_text) > 60 else ''}")
        
        print(f"\nFound {len(results)} headings!")
        
        # Save files if requested
        if save_files:
            save_results(results, url)
        
        return results
        
    except Exception as e:
        print(f"\nScraping failed: {str(e)}")
        print("Common issues:")
        print("- Site blocked the scraper (try changing USER_AGENT)")
        print("- Network problems (check your connection)")
        print("- Page structure changed (inspect element to verify)")
        return []

def save_results(data, source_url):
    """Helper to save our scraped data to files"""
    if not data:
        return
    
    # Create a clean filename from the URL
    site_name = source_url.split('//')[-1].split('/')[0].replace('.', '_')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    base_name = f"{site_name}_headings_{timestamp}"
    
    try:
        # Save CSV
        csv_file = f"{base_name}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved CSV: {csv_file}")
        
        # Save JSON
        json_file = f"{base_name}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved JSON: {json_file}")
        
    except Exception as e:
        print(f"Failed to save files: {str(e)}")

if __name__ == "__main__":
    # Example usage - edit these values!
    TARGET_URL = "https://example.com"  # Change this to your target site
    HEADING_TAG = "h2"  # Try "h1" or "h3" if you want different headings
    REQUEST_DELAY = 2  # Seconds between requests
    
    print("\n=== Simple Web Scraper ===")
    print(f"Configuration:\n- URL: {TARGET_URL}\n- Tag: {HEADING_TAG}\n- Delay: {REQUEST_DELAY}s\n")
    
    scraped_data = scrape_site(
        url=TARGET_URL,
        heading_type=HEADING_TAG,
        pause=REQUEST_DELAY
    )
    
    print("\nDone! Here's a sample of what we found:")
    if scraped_data:
        for item in scraped_data[:3]:  # Show first 3 as preview
            print(f"  {item['order']}. {item['text'][:50]}...")
    else:
        print("No data was scraped - check the messages above for issues")
