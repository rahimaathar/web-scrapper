
# Friendly Web Scraper 

Welcome! This is a simple, friendly web scraper built with Python. It’s designed to help you gather useful content from websites in a polite and respectful way.

## What It Does

- Scrapes not just headings (like h1, h2), but also paragraphs and links.
- Saves the scraped content in easy-to-use CSV and JSON files.
- Adds polite pauses between requests to avoid hammering websites.
- Tries to behave like a real browser by using a user-agent header.
- Includes tips to stay ethical and avoid getting blocked.

## Why I Built This

I made this scraper to help with content analysis, SEO research, and general web exploration — without the complexity or headaches. It’s a lightweight tool for when you need quick insights from web pages.

## How to Use

1. Set the `TARGET_URL` in the script to the website you want to scrape.
2. Choose which HTML elements to scrape (`h1`, `h2`, `p`, `a`, etc.).
3. Run the script and watch it work its magic.
4. Find your results neatly saved in CSV and JSON files named after the site and timestamp.

## Quick Tips for Good Scraping

- Always check the site's `robots.txt` to respect their rules.
- Add delays (the script defaults to 2 seconds) so you don’t overload servers.
- If you get blocked, try changing the user-agent string.
- Use scraping responsibly and ethically.

## Example

```python
TARGET_URL = "https://example.com"
ELEMENTS_TO_SCRAPE = ['h1', 'h2', 'p', 'a']
REQUEST_DELAY = 2  # seconds
```
## How to start

1. **Set up the environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run app**:
   ```bash
   python app.py
  

Run the script, and you’ll get files like `example_com_content_20230531-150000.csv` with all your scraped data.

## Thanks for stopping by!

Feel free to use and modify this tool however you like. Happy scraping! 
