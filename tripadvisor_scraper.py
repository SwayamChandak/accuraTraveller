"""
TripAdvisor Web Scraper - Generalized scraper for extracting information from any TripAdvisor page
Uses BeautifulSoup4 for parsing and is designed for LLM integration
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
import json
import time
from urllib.parse import urljoin, urlparse
import re


class TripAdvisorScraper:
    """
    A generalized web scraper for TripAdvisor pages.
    Designed to extract structured information that can be fed to LLMs.
    """
    
    def __init__(self, delay: float = 2.0):
        """
        Initialize the scraper with optional delay between requests.
        
        Args:
            delay: Delay in seconds between requests to be respectful to the server
        """
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            time.sleep(self.delay)  # Be respectful to the server
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract all text content from the page in a structured format.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Dictionary containing structured text content
        """
        data = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'lists': [],
            'metadata': {}
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            data['title'] = title_tag.get_text(strip=True)
        
        # Extract all headings (h1-h6)
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                text = heading.get_text(strip=True)
                if text:
                    data['headings'].append({
                        'level': i,
                        'text': text
                    })
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                data['paragraphs'].append(text)
        
        # Extract lists
        lists = soup.find_all(['ul', 'ol'])
        for lst in lists:
            items = [li.get_text(strip=True) for li in lst.find_all('li')]
            if items:
                data['lists'].append({
                    'type': lst.name,
                    'items': items
                })
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                data['metadata'][name] = content
        
        return data
    
    def extract_reviews(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract reviews from the page (common pattern on TripAdvisor).
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of review dictionaries
        """
        reviews = []
        
        # Common review containers (TripAdvisor uses different class names over time)
        review_containers = soup.find_all(['div', 'article'], 
                                         class_=re.compile(r'review|Review'))
        
        for container in review_containers:
            review_data = {}
            
            # Extract rating (look for SVG, span with rating info)
            rating_elem = container.find(['span', 'div'], 
                                        class_=re.compile(r'rating|Rating|bubble'))
            if rating_elem:
                # Try to extract rating from class or aria-label
                rating_text = rating_elem.get('class', [])
                aria_label = rating_elem.get('aria-label', '')
                review_data['rating'] = self._extract_rating(str(rating_text) + ' ' + aria_label)
            
            # Extract review title
            title_elem = container.find(['div', 'span', 'a'], 
                                       class_=re.compile(r'title|Title'))
            if title_elem:
                review_data['title'] = title_elem.get_text(strip=True)
            
            # Extract review text
            text_elem = container.find(['div', 'span', 'p'], 
                                      class_=re.compile(r'text|Text|partial_entry'))
            if text_elem:
                review_data['text'] = text_elem.get_text(strip=True)
            
            # Extract date
            date_elem = container.find(['span', 'div'], 
                                      class_=re.compile(r'date|Date|ratingDate'))
            if date_elem:
                review_data['date'] = date_elem.get_text(strip=True)
            
            # Extract author
            author_elem = container.find(['div', 'span', 'a'], 
                                        class_=re.compile(r'username|member|author'))
            if author_elem:
                review_data['author'] = author_elem.get_text(strip=True)
            
            if review_data:  # Only add if we found some data
                reviews.append(review_data)
        
        return reviews
    
    def extract_ratings_summary(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract overall ratings and rating distribution.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Dictionary with rating information
        """
        ratings = {
            'overall_rating': None,
            'total_reviews': None,
            'rating_distribution': {}
        }
        
        # Look for overall rating
        rating_elem = soup.find(['span', 'div'], 
                               class_=re.compile(r'overall.*rating|rating.*overall', re.I))
        if rating_elem:
            text = rating_elem.get_text(strip=True)
            ratings['overall_rating'] = self._extract_rating(text)
        
        # Look for total review count
        count_elem = soup.find(['span', 'div'], 
                              class_=re.compile(r'review.*count|count.*review|reviewCount', re.I))
        if count_elem:
            text = count_elem.get_text(strip=True)
            ratings['total_reviews'] = self._extract_number(text)
        
        return ratings
    
    def extract_amenities(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract amenities/features from the page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of amenities
        """
        amenities = []
        
        # Look for common amenity containers
        amenity_containers = soup.find_all(['div', 'span', 'li'], 
                                          class_=re.compile(r'amenity|amenities|feature', re.I))
        
        for elem in amenity_containers:
            text = elem.get_text(strip=True)
            if text and len(text) < 100:  # Filter out long text that's not an amenity
                amenities.append(text)
        
        return list(set(amenities))  # Remove duplicates
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[str]]:
        """
        Extract all links from the page, categorized by type.
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links
            
        Returns:
            Dictionary with categorized links
        """
        links = {
            'internal': [],
            'external': [],
            'images': []
        }
        
        # Extract text links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(base_url, href)
            
            # Check if internal or external
            if 'tripadvisor' in urlparse(absolute_url).netloc or not urlparse(absolute_url).netloc:
                links['internal'].append(absolute_url)
            else:
                links['external'].append(absolute_url)
        
        # Extract image links
        for img_tag in soup.find_all('img', src=True):
            links['images'].append(urljoin(base_url, img_tag['src']))
        
        # Remove duplicates
        for key in links:
            links[key] = list(set(links[key]))
        
        return links
    
    def extract_location_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract location/address information.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Dictionary with location information
        """
        location = {
            'address': None,
            'city': None,
            'country': None,
            'coordinates': {}
        }
        
        # Look for address
        address_elem = soup.find(['span', 'div', 'address'], 
                                class_=re.compile(r'address|location|street', re.I))
        if address_elem:
            location['address'] = address_elem.get_text(strip=True)
        
        # Look for schema.org structured data
        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'address' in data:
                        location['address'] = data['address']
                    if 'geo' in data:
                        location['coordinates'] = data['geo']
            except:
                pass
        
        return location
    
    def scrape_page(self, url: str) -> Dict[str, Any]:
        """
        Main method to scrape a TripAdvisor page and extract all available information.
        
        Args:
            url: The URL of the TripAdvisor page to scrape
            
        Returns:
            Dictionary containing all extracted information
        """
        print(f"Scraping: {url}")
        
        soup = self.fetch_page(url)
        if not soup:
            return {'error': 'Failed to fetch page'}
        
        # Extract all information
        result = {
            'url': url,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'content': self.extract_text_content(soup),
            'reviews': self.extract_reviews(soup),
            'ratings': self.extract_ratings_summary(soup),
            'amenities': self.extract_amenities(soup),
            'location': self.extract_location_info(soup),
            'links': self.extract_links(soup, url)
        }
        
        return result
    
    def scrape_multiple_pages(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape multiple pages.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of dictionaries containing extracted information
        """
        results = []
        for url in urls:
            result = self.scrape_page(url)
            results.append(result)
        return results
    
    def save_to_json(self, data: Dict[str, Any], filename: str):
        """
        Save scraped data to a JSON file.
        
        Args:
            data: Data to save
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def format_for_llm(self, data: Dict[str, Any]) -> str:
        """
        Format scraped data into a clean text format suitable for LLM input.
        
        Args:
            data: Scraped data dictionary
            
        Returns:
            Formatted string for LLM
        """
        output = []
        
        # Add title
        if data.get('content', {}).get('title'):
            output.append(f"TITLE: {data['content']['title']}\n")
        
        # Add headings
        if data.get('content', {}).get('headings'):
            output.append("HEADINGS:")
            for heading in data['content']['headings']:
                output.append(f"  {'#' * heading['level']} {heading['text']}")
            output.append("")
        
        # Add ratings
        if data.get('ratings'):
            output.append("RATINGS:")
            if data['ratings'].get('overall_rating'):
                output.append(f"  Overall: {data['ratings']['overall_rating']}")
            if data['ratings'].get('total_reviews'):
                output.append(f"  Total Reviews: {data['ratings']['total_reviews']}")
            output.append("")
        
        # Add location
        if data.get('location', {}).get('address'):
            output.append(f"LOCATION: {data['location']['address']}\n")
        
        # Add amenities
        if data.get('amenities'):
            output.append("AMENITIES:")
            for amenity in data['amenities'][:20]:  # Limit to avoid too much data
                output.append(f"  - {amenity}")
            output.append("")
        
        # Add reviews
        if data.get('reviews'):
            output.append("REVIEWS:")
            for i, review in enumerate(data['reviews'][:10], 1):  # Limit to 10 reviews
                output.append(f"\nReview {i}:")
                if review.get('rating'):
                    output.append(f"  Rating: {review['rating']}")
                if review.get('title'):
                    output.append(f"  Title: {review['title']}")
                if review.get('text'):
                    output.append(f"  Text: {review['text'][:200]}...")  # Truncate long reviews
                if review.get('date'):
                    output.append(f"  Date: {review['date']}")
            output.append("")
        
        # Add main content
        if data.get('content', {}).get('paragraphs'):
            output.append("MAIN CONTENT:")
            for para in data['content']['paragraphs'][:10]:  # Limit paragraphs
                if len(para) > 50:  # Only include substantial paragraphs
                    output.append(f"  {para}\n")
        
        return "\n".join(output)
    
    # Helper methods
    def _extract_rating(self, text: str) -> Optional[float]:
        """Extract numeric rating from text."""
        match = re.search(r'(\d+\.?\d*)\s*(?:of|out of)?\s*\d+', text)
        if match:
            return float(match.group(1))
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Extract numeric value from text."""
        # Remove commas and extract number
        text = text.replace(',', '')
        match = re.search(r'(\d+)', text)
        if match:
            return int(match.group(1))
        return None


# Example usage
if __name__ == "__main__":
    # Initialize scraper
    scraper = TripAdvisorScraper(delay=2.0)
    
    # Example URL (replace with actual TripAdvisor URL)
    url = "https://www.tripadvisor.com/Hotel_Review-g293860-d302088-Reviews-The_Oberoi_Udaivilas-Udaipur_Udaipur_District_Rajasthan.html"
    
    # Scrape the page
    data = scraper.scrape_page(url)
    
    # Save to JSON
    scraper.save_to_json(data, 'tripadvisor_data.json')
    
    # Format for LLM
    llm_input = scraper.format_for_llm(data)
    
    # Save LLM-formatted text
    with open('tripadvisor_llm_input.txt', 'w', encoding='utf-8') as f:
        f.write(llm_input)
    
    print("\n" + "="*50)
    print("LLM-Formatted Output Preview:")
    print("="*50)
    print(llm_input[:1000])  # Print first 1000 characters
