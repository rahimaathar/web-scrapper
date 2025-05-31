import requests
from bs4 import BeautifulSoup
import time
import csv
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.64 Safari/537.36'
}

def scrape_site(url, tags=['h1', 'h2', 'p', 'a', 'img'], pause=2, save_files=True):
    """
    Let's grab some content from a webpage in a friendly way!
    
    Args:
        url (str): The webpage you want to explore.
        tags (list): Which HTML tags you'd like to check out.
        pause (int): How long to wait before we knock on the site's door.
        save_files (bool): Should we keep a copy of what we find? 
    
    Returns:
        dict: Organized treasures by tag name.
    """
    print(f"\nStarting our little adventure on: {url}")
    print(f"We'll be hunting for these tags: {tags}")
    print(f"Taking a moment to be polite... waiting {pause} seconds before we begin.\n")
    
    try:
        time.sleep(pause)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        if 'text/html' not in response.headers.get('Content-Type', ''):
            print("Hmm, looks like we didn’t get a webpage back. It might be a redirect or something else.")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        results = {}

        for tag in tags:
            print(f"Looking for <{tag}> tags...")
            elements = soup.find_all(tag)

            if not elements:
                print(f"  Hmm, no <{tag}> tags found here. Moving on...\n")
                results[tag] = []
                continue

            found_items = []
            for i, elem in enumerate(elements, 1):
                if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
                    text = elem.get_text(strip=True)
                    found_items.append({'order': i, 'type': tag, 'text': text, 'url': url})
                elif tag == 'a':
                    text = elem.get_text(strip=True)
                    href = elem.get('href')
                    found_items.append({'order': i, 'type': tag, 'text': text, 'href': href, 'url': url})
                elif tag == 'img':
                    alt = elem.get('alt') or 'No alt text'
                    src = elem.get('src')
                    found_items.append({'order': i, 'type': tag, 'alt': alt, 'src': src, 'url': url})

            results[tag] = found_items
            print(f"  Yay! Found {len(found_items)} <{tag}> elements.\n")

        if save_files:
            print("Saving what we found so you can keep it for later...")
            for tag, data in results.items():
                save_results(data, url, tag)
            print("All done saving!\n")

        print("Our little exploration is complete! Here's a quick peek at what we discovered:\n")
        for tag, items in results.items():
            print(f"<{tag}> - {len(items)} items found. Sample:")
            for item in items[:2]:
                if tag == 'a':
                    print(f"  {item['order']}. '{item['text']}' --> {item.get('href', 'No link')}")
                elif tag == 'img':
                    print(f"  {item['order']}. Image with alt text: '{item['alt']}' and source: {item.get('src', 'No src')}")
                else:
                    print(f"  {item['order']}. {item.get('text', '')[:60]}{'...' if len(item.get('text','')) > 60 else ''}")
            print()
        
        return results

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        print("Try checking:")
        print("- Is the website URL correct and reachable?")
        print("- Is your internet connection stable?")
        print("- Maybe the site is blocking scrapers? Try changing the user-agent string.")
        return {}

def save_results(data, source_url, tag_name):
    if not data:
        return
    
    site_name = source_url.split('//')[-1].split('/')[0].replace('.', '_')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    base_name = f"{site_name}_{tag_name}_scrape_{timestamp}"
    
    try:
        csv_file = f"{base_name}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            keys = data[0].keys()
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"  Saved a CSV file: {csv_file}")

        json_file = f"{base_name}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Saved a JSON file: {json_file}")

    except Exception as e:
        print(f"  Hmm, couldn't save files for <{tag_name}>: {e}")

if __name__ == "__main__":
    TARGET_URL = "https://example.com"
    TAGS_TO_SCRAPE = ['h1', 'h2', 'p', 'a', 'img']
    DELAY = 2

    print("\n=== Welcome to Your Friendly Web Scraper ===")
    print(f"Here's what we have planned:")
    print(f"- Target URL: {TARGET_URL}")
    print(f"- Tags to find: {TAGS_TO_SCRAPE}")
    print(f"- Pause between requests: {DELAY} seconds\n")

    scrape_site(TARGET_URL, tags=TAGS_TO_SCRAPE, pause=DELAY)
