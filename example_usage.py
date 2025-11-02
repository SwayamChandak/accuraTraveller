"""
Thrillophilia Web Scraper - Example Usage
This demonstrates how to scrape Thrillophilia pages and prepare data for LLM analysis
"""

import json
import requests
from bs4 import BeautifulSoup
import time


def basic_scraping_example():
    """Scrape Thrillophilia 'Things to Do' page and extract all attractions."""
    print("Example 1: Thrillophilia Scraping - Things to Do in Pune")
    print("-" * 50)
    
    # Thrillophilia Pune attractions page
    url = "https://www.thrillophilia.com/things-to-do-in-pune"
    
    # Headers to bypass 403 error
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    
    # Use a session for better connection handling
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Add a small delay to be respectful
        time.sleep(2)
        
        # Make the request
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # List to store all attractions
        attractions = []
        
        # Extract the main heading (h1 with class "constructed-heading")
        main_heading_div = soup.find('h1', class_='constructed-heading')
        
        if main_heading_div:
            # Extract the count/value
            count_span = main_heading_div.find('span', class_='value')
            count = count_span.get_text(strip=True) if count_span else ''
            
            # Extract the title
            title_div = main_heading_div.find('h3', class_='h3 title')
            if title_div:
                title_span = title_div.find('span', class_='title')
                title = title_span.get_text(strip=True) if title_span else 'No title found'
            else:
                title = 'No title found'
            
            # Combine count and title
            page_title = f"{count} {title}".strip()
        else:
            page_title = 'No title found'
        
        print(f"\nPage Title: {page_title}")
        print(f"\n{'='*50}")
        
        # Extract the main post holder div
        post_holder = soup.find('div', class_='post-holder', itemprop='articleBody')
        
        if post_holder:
            # Find all post cards
            post_cards = post_holder.find_all('div', class_='base-block main-card-container content-main-card')
            
            print(f"\nFound {len(post_cards)} things to do in Pune")
            print(f"{'='*50}\n")
            
            # Extract data from each post
            for post_card in post_cards:
                post_data = {}
                
                # Get data-id attribute
                post_id = post_card.get('data-id', 'No ID')
                post_data['id'] = post_id
                
                # Find the left-side div with number
                left_side = post_card.find('div', class_='left-side')
                if left_side:
                    number_span = left_side.find('span', class_='number')
                    if number_span:
                        post_data['number'] = number_span.get_text(strip=True)
                
                # Find the h3 title (class with space: "h3 title")
                title_h3 = post_card.find('h3', class_='h3 title')
                if title_h3:
                    post_data['title'] = title_h3.get_text(strip=True)
                else:
                    post_data['title'] = 'No title found'
                
                # Find text content from text-holder read-more-wrap div
                text_holder = post_card.find('div', class_='text-holder read-more-wrap')
                if text_holder:
                    # Get all paragraphs
                    paragraphs = text_holder.find_all('p')
                    paragraphs_text = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                    
                    # Get all span elements
                    spans = text_holder.find_all('span')
                    spans_text = [span.get_text(strip=True) for span in spans if span.get_text(strip=True)]
                    
                    # Combine all text content
                    all_text = paragraphs_text + spans_text
                    
                    if all_text:
                        post_data['content'] = {
                            'paragraphs': paragraphs_text,
                            'spans': spans_text,
                            'full_text': ' '.join(all_text)
                        }
                    else:
                        # Fallback to getting all text from the div
                        post_data['content'] = {
                            'paragraphs': [],
                            'spans': [],
                            'full_text': text_holder.get_text(strip=True, separator=' ')
                        }
                else:
                    post_data['content'] = {
                        'paragraphs': [],
                        'spans': [],
                        'full_text': 'No content found'
                    }
                
                # Find images
                img_div = post_card.find('div', class_='image')
                if img_div:
                    img_tag = img_div.find('img')
                    if img_tag:
                        post_data['image_url'] = img_tag.get('src', '') or img_tag.get('data-src', '')
                        post_data['image_alt'] = img_tag.get('alt', '')
                
                # Find any links
                link_tag = post_card.find('a')
                if link_tag:
                    href = link_tag.get('href', '')
                    if href:
                        full_url = f"https://www.thrillophilia.com{href}" if href.startswith('/') else href
                        post_data['link'] = full_url
                
                # Add to attractions list
                attractions.append(post_data)
            
            # Save all data to JSON file
            json_data = {
                'page_title': page_title,
                'url': url,
                'total_attractions': len(attractions),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'attractions': attractions
            }
            
            # Save to JSON file
            with open('thrillophilia_pune_attractions.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(attractions)} attractions to 'thrillophilia_pune_attractions.json'")
            print(f"\n{'='*50}")
            print("First 10 Attractions:")
            print(f"{'='*50}\n")
            
            # Display first 10 attractions
            for i, attraction in enumerate(attractions[:10], 1):
                print(f"{i}. [{attraction.get('number', 'N/A')}] {attraction.get('title', 'No title')}")
                if attraction.get('description'):
                    desc = attraction['description'][:100] + '...' if len(attraction.get('description', '')) > 100 else attraction.get('description', '')
                    print(f"   Description: {desc}")
                if attraction.get('link'):
                    print(f"   Link: {attraction['link']}")
                print()
        else:
            print("\nPost holder div not found on the page.")
        
        # Return the data structure
        result = {
            'page_title': page_title,
            'url': url,
            'total_attractions': len(attractions),
            'attractions': attractions
        }
        
        return result
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("\n⚠️  403 Forbidden Error - Thrillophilia is blocking the request")
            print("\nPossible solutions:")
            print("1. Try using a VPN or proxy")
            print("2. Use Selenium with a real browser (headless or visible)")
            print("3. Add random delays between requests")
            print("4. Try from a different IP address")
            print("\nFor now, try using Selenium - see selenium_scraper.py")
        else:
            print(f"\nHTTP Error: {e}")
        return None
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        return None


def multiple_pages_example():
    """Example of scraping multiple Thrillophilia city pages."""
    print("\n\nExample 2: Scraping Multiple Thrillophilia Pages")
    print("-" * 50)
    
    # List of Thrillophilia URLs to scrape
    urls = [
        "https://www.thrillophilia.com/things-to-do-in-pune",
        "https://www.thrillophilia.com/things-to-do-in-mumbai",
    ]
    
    # You can implement multi-page scraping here
    print("Multi-page scraping: Loop through URLs and call basic_scraping_example() for each")
    
    return None


def llm_integration_example():
    """Example of preparing Thrillophilia data for LLM analysis."""
    print("\n\nExample 3: LLM Integration with Thrillophilia Data")
    print("-" * 50)
    
    # Load the scraped JSON data
    try:
        with open('thrillophilia_pune_attractions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Format for LLM
        llm_prompt = f"Here are {data['total_attractions']} things to do in Pune:\n\n"
        
        for attraction in data['attractions'][:5]:  # First 5 for example
            llm_prompt += f"{attraction.get('number', '')}. {attraction['title']}\n"
            if attraction.get('content'):
                llm_prompt += f"   {attraction['content']['full_text'][:200]}...\n\n"
        
        print("Formatted text for LLM (first 500 chars):")
        print(llm_prompt[:500])
        
        # Save for LLM processing
        with open('thrillophilia_llm_input.txt', 'w', encoding='utf-8') as f:
            f.write(llm_prompt)
        
        print("\n\nSaved to thrillophilia_llm_input.txt")
        
        return llm_prompt
    except FileNotFoundError:
        print("Error: thrillophilia_pune_attractions.json not found. Run basic_scraping_example() first.")
        return None


def custom_extraction_example():
    """Example of extracting specific fields from Thrillophilia data."""
    print("\n\nExample 4: Custom Data Extraction")
    print("-" * 50)
    
    # Load the scraped JSON data
    try:
        with open('thrillophilia_pune_attractions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract only titles and links
        titles_and_links = [
            {
                'title': attraction['title'],
                'link': attraction.get('link', 'No link')
            }
            for attraction in data['attractions']
        ]
        
        print(f"Extracted {len(titles_and_links)} titles and links")
        for item in titles_and_links[:5]:
            print(f"  - {item['title']}")
        
        return titles_and_links
    except FileNotFoundError:
        print("Error: thrillophilia_pune_attractions.json not found. Run basic_scraping_example() first.")
        return None


def search_specific_content_example():
    """Example of searching for specific keywords in Thrillophilia content."""
    print("\n\nExample 5: Search Specific Content")
    print("-" * 50)
    
    # Load the scraped JSON data
    try:
        with open('thrillophilia_pune_attractions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Search for attractions mentioning specific keywords
        keywords = ['camping', 'adventure', 'historical']
        
        for keyword in keywords:
            matching_attractions = [
                attraction for attraction in data['attractions']
                if attraction.get('content') and keyword.lower() in attraction['content']['full_text'].lower()
            ]
            print(f"\nAttractions mentioning '{keyword}': {len(matching_attractions)}")
    except FileNotFoundError:
        print("Error: thrillophilia_pune_attractions.json not found. Run basic_scraping_example() first.")
        return None


def save_structured_data_example():
    """Example of saving Thrillophilia data in different formats."""
    print("\n\nExample 6: Save Structured Data")
    print("-" * 50)
    
    # Load the scraped JSON data
    try:
        with open('thrillophilia_pune_attractions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Save only titles
        titles_only = {
            'page_title': data['page_title'],
            'total': data['total_attractions'],
            'titles': [attraction['title'] for attraction in data['attractions']]
        }
        
        with open('thrillophilia_titles_only.json', 'w', encoding='utf-8') as f:
            json.dump(titles_only, f, indent=2, ensure_ascii=False)
        
        print("Data saved in different formats:")
        print("  - thrillophilia_pune_attractions.json (complete data)")
        print("  - thrillophilia_titles_only.json (titles only)")
    except FileNotFoundError:
        print("Error: thrillophilia_pune_attractions.json not found. Run basic_scraping_example() first.")
        return None


if __name__ == "__main__":
    print("Thrillophilia Scraper - Example Usage")
    print("=" * 50)
    print("\nThis scraper extracts 'Things to Do' data from Thrillophilia")
    print("Currently configured for: Things to Do in Pune\n")
    
    # Run the Thrillophilia scraper
    basic_scraping_example()
    
    print("\n\nScraping completed! Check 'thrillophilia_pune_attractions.json' for full data")

