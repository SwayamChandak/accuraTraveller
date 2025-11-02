from bs4 import BeautifulSoup
import requests
import json
import time

url = 'https://www.booking.com/searchresults.html?ss=North+Goa%2C+India&ssne=New+Delhi&ssne_untouched=New+Delhi&efdco=1&label=mkt123sc-84161719-39d8-45e4-a8c3-7fb7332816cc&aid=331424&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=5052&dest_type=region&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=91b10a26e02a40bccd97d778788b32aa&ac_meta=GiA5MWIxMGEyNmUwMmE0MGJjY2Q5N2Q3Nzg3ODhiMzJhYSABKAEyAmVuOgNnb2FAAEoAUAA%3D&checkin=2025-12-13&checkout=2025-12-15&group_adults=2&no_rooms=1&group_children=0'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response  = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all the hotel elements in the HTML document
hotels = soup.find_all('div', {'data-testid': 'property-card'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip() if name_element else 'N/A'

    # Extract the hotel location
    location_element = hotel.find('span', {'data-testid': 'address'})
    location = location_element.text.strip() if location_element else 'N/A'

    # Extract the hotel price
    price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    price = price_element.text.strip() if price_element else 'N/A'
    
    # Extract the hotel rating by counting filled star divs
    rating = 'N/A'
    rating_container = hotel.find('div', {'data-testid': 'rating-stars'})
    if rating_container:
        # Count divs with class containing "e0397"
        filled_stars = rating_container.find_all('div', class_=lambda x: x and 'e0397' in str(x))
        if filled_stars:
            rating = f"{len(filled_stars)}/5"
    
    # Append hotes_data with info about hotel
    hotels_data.append({
        'name': name,
        'location': location,
        'price': price,
        'rating': rating
    })

# Print summary
print(f"\nScraped {len(hotels_data)} hotels successfully!")
print("=" * 50)
print("First 5 Hotels:")
print("=" * 50 + "\n")

# Display first 5 hotels
for i, hotel in enumerate(hotels_data[:5], 1):
    print(f"{i}. {hotel['name']}")
    print(f"   Location: {hotel['location']}")
    print(f"   Price: {hotel['price']}")
    print(f"   Rating: {hotel['rating']}")
    print()

# Create structured JSON data
json_data = {
    'search_url': url,
    'total_hotels': len(hotels_data),
    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
    'hotels': hotels_data
}

# Save to JSON file
with open('booking_hotels.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print(f"✅ Data saved to 'booking_hotels.json'")
print(f"Total hotels: {len(hotels_data)}")