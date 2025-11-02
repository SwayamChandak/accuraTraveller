"""
Booking.com Web Scraper
Scrapes hotel listings and details from Booking.com
Designed for LLM integration and travel planning
"""

import json
import requests
from bs4 import BeautifulSoup
import time


def scrape_booking_hotels(url):
    """
    Scrape hotel listings from Booking.com search results page.
    
    Args:
        url: Booking.com search URL (e.g., hotels in a city)
    
    Returns:
        Dictionary containing all scraped hotel data
    """
    print("Booking.com Hotel Scraper")
    print("-" * 50)
    
    # Headers to mimic a real browser and avoid blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Use a session for better connection handling
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Add delay to be respectful to the server
        time.sleep(2)
        
        # Make the request
        print(f"\nFetching: {url}")
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # List to store all hotels
        hotels = []
        
        # Extract page title
        page_title = soup.find('title')
        title = page_title.get_text(strip=True) if page_title else 'No title found'
        
        print(f"Page Title: {title}\n")
        print("=" * 50)
        
        # Find all hotel cards/listings
        # Booking.com commonly uses these selectors (may need adjustment based on current structure)
        hotel_cards = soup.find_all('div', attrs={'data-testid': 'property-card'})
        
        # Alternative selectors if above doesn't work
        if not hotel_cards:
            hotel_cards = soup.find_all('div', class_=lambda x: x and 'property-card' in x.lower())
        
        if not hotel_cards:
            # Try another common pattern
            hotel_cards = soup.find_all('div', attrs={'data-testid': lambda x: x and 'property' in str(x).lower()})
        
        print(f"Found {len(hotel_cards)} hotel listings\n")
        
        # Extract data from each hotel card
        for idx, card in enumerate(hotel_cards, 1):
            hotel_data = {
                'id': idx,
                'name': None,
                'price': None,
                'rating': None,
                'review_score': None,
                'review_count': None,
                'location': None,
                'distance': None,
                'amenities': [],
                'image_url': None,
                'link': None
            }
            
            # Extract hotel name
            # Common patterns for hotel names
            name_elem = (
                card.find('div', attrs={'data-testid': 'title'}) or
                card.find('h3') or
                card.find('div', class_=lambda x: x and 'title' in str(x).lower())
            )
            if name_elem:
                hotel_data['name'] = name_elem.get_text(strip=True)
            
            # Extract price
            price_elem = (
                card.find('span', attrs={'data-testid': 'price-and-discounted-price'}) or
                card.find('div', class_=lambda x: x and 'price' in str(x).lower())
            )
            if price_elem:
                hotel_data['price'] = price_elem.get_text(strip=True)
            
            # Extract rating/score
            rating_elem = (
                card.find('div', attrs={'data-testid': 'review-score'}) or
                card.find('div', class_=lambda x: x and 'review-score' in str(x).lower())
            )
            if rating_elem:
                hotel_data['rating'] = rating_elem.get_text(strip=True)
            
            # Extract review count
            review_count_elem = card.find('div', attrs={'data-testid': 'review-score-text'})
            if review_count_elem:
                hotel_data['review_count'] = review_count_elem.get_text(strip=True)
            
            # Extract location/address
            location_elem = (
                card.find('span', attrs={'data-testid': 'address'}) or
                card.find('span', class_=lambda x: x and 'address' in str(x).lower())
            )
            if location_elem:
                hotel_data['location'] = location_elem.get_text(strip=True)
            
            # Extract distance from center
            distance_elem = (
                card.find('span', attrs={'data-testid': 'distance'}) or
                card.find('span', class_=lambda x: x and 'distance' in str(x).lower())
            )
            if distance_elem:
                hotel_data['distance'] = distance_elem.get_text(strip=True)
            
            # Extract amenities/facilities
            amenities_container = card.find('div', class_=lambda x: x and 'facility' in str(x).lower())
            if amenities_container:
                amenity_items = amenities_container.find_all(['span', 'div'])
                hotel_data['amenities'] = [item.get_text(strip=True) for item in amenity_items if item.get_text(strip=True)]
            
            # Extract image
            img_elem = card.find('img')
            if img_elem:
                hotel_data['image_url'] = img_elem.get('src') or img_elem.get('data-src')
            
            # Extract link to hotel page
            link_elem = card.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                # Make absolute URL if relative
                if href.startswith('/'):
                    hotel_data['link'] = f"https://www.booking.com{href}"
                elif href.startswith('http'):
                    hotel_data['link'] = href
            
            # Only add if we got at least a name
            if hotel_data['name']:
                hotels.append(hotel_data)
        
        # Create result structure
        result = {
            'page_title': title,
            'url': url,
            'total_hotels': len(hotels),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'hotels': hotels
        }
        
        # Save to JSON file
        output_file = 'booking_hotels.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(hotels)} hotels to '{output_file}'")
        print("\n" + "=" * 50)
        print("First 10 Hotels:")
        print("=" * 50 + "\n")
        
        # Display first 10 hotels
        for hotel in hotels[:10]:
            print(f"{hotel['id']}. {hotel['name']}")
            if hotel['price']:
                print(f"   Price: {hotel['price']}")
            if hotel['rating']:
                print(f"   Rating: {hotel['rating']}")
            if hotel['location']:
                print(f"   Location: {hotel['location']}")
            if hotel['link']:
                print(f"   Link: {hotel['link']}")
            print()
        
        return result
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("\n⚠️  403 Forbidden Error - Booking.com is blocking the request")
            print("\nPossible solutions:")
            print("1. Use Selenium with a real browser (recommended)")
            print("2. Try using a VPN or proxy")
            print("3. Add random delays between requests")
            print("4. Use residential proxies")
            print("\nNote: Booking.com has strong anti-bot protection")
        else:
            print(f"\nHTTP Error: {e}")
        return None
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        return None


def scrape_hotel_details(hotel_url):
    """
    Scrape detailed information from a specific hotel page.
    
    Args:
        hotel_url: Direct URL to a hotel page on Booking.com
    
    Returns:
        Dictionary containing detailed hotel information
    """
    print("\nScraping Hotel Details")
    print("-" * 50)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        time.sleep(2)
        response = session.get(hotel_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        hotel_details = {
            'url': hotel_url,
            'name': None,
            'description': None,
            'facilities': [],
            'room_types': [],
            'policies': {},
            'reviews': []
        }
        
        # Extract hotel name
        name_elem = soup.find('h2', class_=lambda x: x and 'name' in str(x).lower())
        if name_elem:
            hotel_details['name'] = name_elem.get_text(strip=True)
        
        # Extract description
        desc_elem = soup.find('div', attrs={'data-testid': 'property-description'})
        if desc_elem:
            paragraphs = desc_elem.find_all('p')
            hotel_details['description'] = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        # Extract facilities
        facilities_section = soup.find('div', class_=lambda x: x and 'facility' in str(x).lower())
        if facilities_section:
            facility_items = facilities_section.find_all('span')
            hotel_details['facilities'] = [item.get_text(strip=True) for item in facility_items if item.get_text(strip=True)]
        
        print(f"Scraped details for: {hotel_details['name']}")
        
        return hotel_details
        
    except Exception as e:
        print(f"Error scraping hotel details: {e}")
        return None


def format_for_llm(data):
    """
    Format scraped Booking.com data for LLM input.
    
    Args:
        data: Dictionary from scrape_booking_hotels()
    
    Returns:
        Formatted string suitable for LLM processing
    """
    if not data or 'hotels' not in data:
        return "No hotel data available"
    
    output = []
    output.append(f"BOOKING.COM SEARCH RESULTS")
    output.append(f"Total Hotels Found: {data['total_hotels']}\n")
    output.append("=" * 50 + "\n")
    
    for hotel in data['hotels']:
        output.append(f"Hotel: {hotel['name']}")
        
        if hotel['price']:
            output.append(f"Price: {hotel['price']}")
        
        if hotel['rating']:
            output.append(f"Rating: {hotel['rating']}")
        
        if hotel['review_count']:
            output.append(f"Reviews: {hotel['review_count']}")
        
        if hotel['location']:
            output.append(f"Location: {hotel['location']}")
        
        if hotel['distance']:
            output.append(f"Distance from center: {hotel['distance']}")
        
        if hotel['amenities']:
            output.append(f"Amenities: {', '.join(hotel['amenities'][:5])}")
        
        output.append("")
    
    return "\n".join(output)


# Example usage
if __name__ == "__main__":
    # Example: Search for hotels in Pune, India
    # You need to get the actual search URL from Booking.com
    # Go to booking.com, search for your destination, and copy the URL
    
    # Example URL format (replace with actual search URL):
    url = "https://www.booking.com/searchresults.html?ss=North+Goa%2C+India&ssne=New+Delhi&ssne_untouched=New+Delhi&efdco=1&label=mkt123sc-84161719-39d8-45e4-a8c3-7fb7332816cc&aid=331424&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=5052&dest_type=region&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=91b10a26e02a40bccd97d778788b32aa&ac_meta=GiA5MWIxMGEyNmUwMmE0MGJjY2Q5N2Q3Nzg3ODhiMzJhYSABKAEyAmVuOgNnb2FAAEoAUAA%3D&checkin=2025-12-13&checkout=2025-12-15&group_adults=2&no_rooms=1&group_children=0"
    
    print("Booking.com Scraper")
    print("=" * 50)
    print("\n⚠️  IMPORTANT NOTES:")
    print("1. Booking.com has strong anti-bot protection")
    print("2. For best results, use Selenium instead of requests")
    print("3. You may need to solve CAPTCHAs")
    print("4. Use actual search URLs from booking.com")
    print("\nExample URL format:")
    print("https://www.booking.com/searchresults.html?ss=CityName&dest_type=city\n")
    
    # Uncomment to run scraper (make sure to use a valid Booking.com URL)
    result = scrape_booking_hotels(url)
    
    # Format for LLM
    # if result:
    #     llm_input = format_for_llm(result)
    #     with open('booking_llm_input.txt', 'w', encoding='utf-8') as f:
    #         f.write(llm_input)
    #     print("\n✅ LLM-formatted data saved to 'booking_llm_input.txt'")
    
    # print("\n⚠️  Uncomment the code above to run the scraper")
    # print("Make sure to replace the URL with an actual Booking.com search URL")
