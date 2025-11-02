# TripAdvisor Web Scraper

A generalized Python web scraper for extracting information from TripAdvisor pages, designed for easy LLM integration.

## Features

- 🔍 **Generalized Scraping**: Works with any TripAdvisor page (hotels, restaurants, attractions, etc.)
- 📊 **Structured Data Extraction**: Extracts reviews, ratings, amenities, location info, and more
- 🤖 **LLM-Ready**: Formats data specifically for Large Language Model integration
- 🎯 **Modular Design**: Use individual extraction methods or scrape everything at once
- 💾 **Multiple Output Formats**: Save as JSON or LLM-formatted text
- 🚦 **Rate Limiting**: Built-in delays to respect server resources

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from tripadvisor_scraper import TripAdvisorScraper

# Initialize scraper
scraper = TripAdvisorScraper(delay=2.0)

# Scrape a page
url = "https://www.tripadvisor.com/[YOUR-TRIPADVISOR-URL]"
data = scraper.scrape_page(url)

# Save results
scraper.save_to_json(data, 'output.json')

# Format for LLM
llm_input = scraper.format_for_llm(data)
print(llm_input)
```

## What Can Be Extracted?

The scraper extracts:

1. **Text Content**
   - Page title
   - Headings (h1-h6)
   - Paragraphs
   - Lists
   - Meta tags

2. **Reviews**
   - Review text
   - Ratings
   - Titles
   - Dates
   - Authors

3. **Ratings Summary**
   - Overall rating
   - Total review count
   - Rating distribution

4. **Location Information**
   - Address
   - City/Country
   - Coordinates (when available)

5. **Amenities/Features**
   - List of amenities or features mentioned

6. **Links**
   - Internal links
   - External links
   - Image URLs

## Usage Examples

### Basic Scraping

```python
from tripadvisor_scraper import TripAdvisorScraper

scraper = TripAdvisorScraper(delay=2.0)
data = scraper.scrape_page("https://www.tripadvisor.com/...")

print(f"Title: {data['content']['title']}")
print(f"Reviews found: {len(data['reviews'])}")
print(f"Overall rating: {data['ratings']['overall_rating']}")
```

### Scrape Multiple Pages

```python
urls = [
    "https://www.tripadvisor.com/Hotel_Review-...",
    "https://www.tripadvisor.com/Restaurant_Review-...",
    "https://www.tripadvisor.com/Attraction_Review-..."
]

results = scraper.scrape_multiple_pages(urls)
```

### LLM Integration

```python
# Scrape and format for LLM
data = scraper.scrape_page(url)
llm_input = scraper.format_for_llm(data)

# Use with your LLM
# response = your_llm.generate(
#     prompt=f"Analyze this TripAdvisor page:\n\n{llm_input}"
# )
```

### Custom Extraction

```python
# Fetch page once
soup = scraper.fetch_page(url)

# Use specific extraction methods
reviews = scraper.extract_reviews(soup)
ratings = scraper.extract_ratings_summary(soup)
amenities = scraper.extract_amenities(soup)
location = scraper.extract_location_info(soup)
```

### Search Reviews by Keyword

```python
data = scraper.scrape_page(url)

# Find reviews mentioning specific keywords
keyword = "service"
matching_reviews = [
    review for review in data['reviews']
    if keyword.lower() in review.get('text', '').lower()
]

print(f"Found {len(matching_reviews)} reviews mentioning '{keyword}'")
```

## Output Format

### JSON Structure

```json
{
  "url": "https://www.tripadvisor.com/...",
  "scraped_at": "2025-11-02 10:30:00",
  "content": {
    "title": "Page Title",
    "headings": [...],
    "paragraphs": [...],
    "lists": [...],
    "metadata": {...}
  },
  "reviews": [
    {
      "rating": 5.0,
      "title": "Review Title",
      "text": "Review text...",
      "date": "October 2025",
      "author": "Username"
    }
  ],
  "ratings": {
    "overall_rating": 4.5,
    "total_reviews": 1234
  },
  "amenities": [...],
  "location": {...},
  "links": {...}
}
```

### LLM-Formatted Text

The scraper formats data into clean, readable text perfect for LLM prompts:

```
TITLE: Hotel Name - TripAdvisor

HEADINGS:
  # Main Heading
  ## Sub Heading

RATINGS:
  Overall: 4.5
  Total Reviews: 1234

LOCATION: 123 Main St, City, Country

AMENITIES:
  - Free WiFi
  - Pool
  - Restaurant

REVIEWS:
Review 1:
  Rating: 5.0
  Title: Amazing experience
  Text: This place was wonderful...
  Date: October 2025
...
```

## Advanced Features

### Rate Limiting

The scraper includes built-in delays between requests:

```python
# Adjust delay (in seconds) when initializing
scraper = TripAdvisorScraper(delay=3.0)  # 3 second delay
```

### Custom Headers

The scraper uses realistic browser headers to avoid blocks. Headers are configured automatically.

### Error Handling

The scraper handles common errors gracefully:

```python
data = scraper.scrape_page(url)
if 'error' in data:
    print(f"Scraping failed: {data['error']}")
```

## LLM Integration Ideas

1. **Sentiment Analysis**: Analyze review sentiment
2. **Summary Generation**: Create summaries of all reviews
3. **Question Answering**: Answer questions about the location
4. **Comparison**: Compare multiple locations
5. **Recommendation**: Generate personalized recommendations
6. **Translation**: Translate reviews to other languages
7. **Trend Analysis**: Identify common themes in reviews

## Important Notes

⚠️ **Legal and Ethical Considerations**:
- Always check TripAdvisor's Terms of Service
- Respect robots.txt
- Use appropriate delays between requests
- Don't overload their servers
- Consider using TripAdvisor's official API if available
- Only scrape public data
- Comply with data protection regulations

## Tips for Best Results

1. **Use Specific URLs**: Works best with specific listing pages (hotels, restaurants, attractions)
2. **Check Robots.txt**: Verify that scraping is allowed
3. **Handle Dynamic Content**: Some content may load via JavaScript (consider using Selenium for such cases)
4. **Regular Updates**: TripAdvisor may change their HTML structure; update selectors as needed
5. **Error Handling**: Always check if data extraction succeeded

## Troubleshooting

**No data extracted?**
- Check if the URL is valid
- TripAdvisor may have changed their HTML structure
- Try updating the class name patterns in the code

**Getting blocked?**
- Increase the delay between requests
- Use a proxy or VPN
- Reduce the number of requests

**Missing reviews?**
- Reviews may load dynamically via JavaScript
- Consider using Selenium for JavaScript-heavy pages

## Future Enhancements

- [ ] Add Selenium support for dynamic content
- [ ] Implement proxy rotation
- [ ] Add caching to avoid re-scraping
- [ ] Support for pagination
- [ ] Export to CSV/Excel
- [ ] GUI interface
- [ ] Direct LLM API integration

## Example Workflow with LLM

```python
# 1. Scrape data
scraper = TripAdvisorScraper()
data = scraper.scrape_page(url)

# 2. Format for LLM
llm_text = scraper.format_for_llm(data)

# 3. Send to LLM (example with OpenAI)
# import openai
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[{
#         "role": "user",
#         "content": f"Analyze this TripAdvisor listing and provide insights:\n\n{llm_text}"
#     }]
# )
# print(response.choices[0].message.content)
```

## Contributing

Feel free to enhance this scraper! Some ideas:
- Add support for more page types
- Improve extraction patterns
- Add tests
- Optimize performance

## License

This is a educational project. Use responsibly and ethically.
