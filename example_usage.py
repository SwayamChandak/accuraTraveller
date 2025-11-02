"""
Example usage of TripAdvisor Scraper with LLM integration
This demonstrates how to use the scraper and prepare data for LLM analysis
"""

from tripadvisor_scraper import TripAdvisorScraper
import json


def basic_scraping_example():
    """Basic example of scraping a single page - extracting 'Places to Visit' section."""
    print("Example 1: Basic Scraping - Places to Visit")
    print("-" * 50)
    
    # Thrillophilia Pune attractions page
    url = "https://www.thrillophilia.com/things-to-do-in-pune"
    
    # Headers to bypass 403 error
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    
    # Use a session for better connection handling
    import requests
    from bs4 import BeautifulSoup
    import time
    
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
            print("\n⚠️  403 Forbidden Error - TripAdvisor is blocking the request")
            print("\nPossible solutions:")
            print("1. Try using a VPN or proxy")
            print("2. Use Selenium with a real browser (headless or visible)")
            print("3. Add random delays between requests")
            print("4. Try from a different IP address")
            print("5. Consider using TripAdvisor's official API if available")
            print("\nFor now, try using Selenium - uncomment the selenium_scraping_example() below")
        else:
            print(f"\nHTTP Error: {e}")
        return None
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        return None


def multiple_pages_example():
    """Example of scraping multiple pages."""
    print("\n\nExample 2: Scraping Multiple Pages")
    print("-" * 50)
    
    scraper = TripAdvisorScraper(delay=2.0)
    
    # List of URLs to scrape
    urls = [
        "https://www.tripadvisor.com/Restaurant_Review-g60763-d423942-Reviews-Katz_s_Delicatessen-New_York_City_New_York.html",
        "https://www.tripadvisor.com/Hotel_Review-g60763-d93452-Reviews-The_Plaza_Hotel-New_York_City_New_York.html",
    ]
    
    results = scraper.scrape_multiple_pages(urls)
    
    print(f"Scraped {len(results)} pages successfully")
    
    return results


def llm_integration_example():
    """Example of preparing data for LLM analysis."""
    print("\n\nExample 3: LLM Integration")
    print("-" * 50)
    
    scraper = TripAdvisorScraper(delay=2.0)
    
    # Scrape a page
    url = "https://www.tripadvisor.com/Attraction_Review-g293860-d3850906-Reviews-Bagore_Ki_Haveli-Udaipur_Udaipur_District_Rajasthan.html"
    data = scraper.scrape_page(url)
    
    # Format for LLM
    llm_input = scraper.format_for_llm(data)
    
    print("Formatted text for LLM (first 500 chars):")
    print(llm_input[:500])
    
    # Save for LLM processing
    with open('llm_input.txt', 'w', encoding='utf-8') as f:
        f.write(llm_input)
    
    print("\n\nSaved to llm_input.txt")
    
    # This is where you would integrate with your LLM
    # Example pseudo-code:
    # llm_response = your_llm.generate(
    #     prompt=f"Analyze this TripAdvisor page and provide insights:\n\n{llm_input}"
    # )
    
    return llm_input


def custom_extraction_example():
    """Example of using custom extraction methods."""
    print("\n\nExample 4: Custom Extraction")
    print("-" * 50)
    
    scraper = TripAdvisorScraper(delay=2.0)
    url = "https://www.tripadvisor.com/Hotel_Review-g293860-d302088-Reviews-The_Oberoi_Udaivilas-Udaipur_Udaipur_District_Rajasthan.html"
    
    # Fetch the page
    soup = scraper.fetch_page(url)
    
    if soup:
        # Use individual extraction methods
        text_content = scraper.extract_text_content(soup)
        reviews = scraper.extract_reviews(soup)
        ratings = scraper.extract_ratings_summary(soup)
        location = scraper.extract_location_info(soup)
        
        print(f"Extracted {len(text_content['headings'])} headings")
        print(f"Extracted {len(reviews)} reviews")
        print(f"Overall rating: {ratings['overall_rating']}")
        print(f"Location: {location['address']}")


def search_specific_content_example():
    """Example of searching for specific content in scraped data."""
    print("\n\nExample 5: Search Specific Content")
    print("-" * 50)
    
    scraper = TripAdvisorScraper(delay=2.0)
    url = "https://www.tripadvisor.com/Restaurant_Review-g293860-d8013938-Reviews-Upre_by_1559_AD-Udaipur_Udaipur_District_Rajasthan.html"
    
    data = scraper.scrape_page(url)
    
    # Search for reviews mentioning specific keywords
    keywords = ['food', 'service', 'ambiance']
    
    for keyword in keywords:
        matching_reviews = [
            review for review in data['reviews']
            if review.get('text') and keyword.lower() in review['text'].lower()
        ]
        print(f"\nReviews mentioning '{keyword}': {len(matching_reviews)}")


def save_structured_data_example():
    """Example of saving data in different formats."""
    print("\n\nExample 6: Save Structured Data")
    print("-" * 50)
    
    scraper = TripAdvisorScraper(delay=2.0)
    url = "https://www.tripadvisor.com/Attraction_Review-g293860-d3850906-Reviews-Bagore_Ki_Haveli-Udaipur_Udaipur_District_Rajasthan.html"
    
    data = scraper.scrape_page(url)
    
    # Save as JSON
    scraper.save_to_json(data, 'scraped_data.json')
    
    # Save reviews separately for easy access
    reviews_only = {
        'url': url,
        'total_reviews': len(data['reviews']),
        'reviews': data['reviews']
    }
    scraper.save_to_json(reviews_only, 'reviews_only.json')
    
    # Save LLM-formatted text
    llm_text = scraper.format_for_llm(data)
    with open('llm_formatted.txt', 'w', encoding='utf-8') as f:
        f.write(llm_text)
    
    print("Data saved in multiple formats:")
    print("  - scraped_data.json (complete data)")
    print("  - reviews_only.json (reviews only)")
    print("  - llm_formatted.txt (LLM-ready text)")


if __name__ == "__main__":
    print("TripAdvisor Scraper - Example Usage")
    print("=" * 50)
    print("\nNote: Replace example URLs with actual TripAdvisor URLs")
    print("These examples demonstrate different use cases\n")
    
    # Run examples (comment out the ones you don't want to run)
    basic_scraping_example()
    # multiple_pages_example()
    # llm_integration_example()
    # custom_extraction_example()
    # search_specific_content_example()
    # save_structured_data_example()
    
    print("\n\nUncomment the examples you want to run in example_usage.py")
