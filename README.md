# AccuraTraveller - AI-Powered Travel Planning Assistant 🌍✈️

An intelligent travel planning system that combines web scraping, LLM-based summarization, and personalized itinerary generation to help users plan perfect trips.

## 🎯 Project Vision

AccuraTraveller aims to be a comprehensive travel planning assistant that:
1. **Personalizes itineraries** based on budget, group size, and location preferences
2. **Scrapes real-time travel data** from multiple sources (attractions, hotels, activities)
3. **Provides live weather updates** for informed decision-making
4. **Predicts travel costs** based on duration, group size, and travel style

---

## ✅ Current Features (Implemented)

### 1. Web Scraping System ✓
- **Thrillophilia Scraper** (`example_usage.py`)
  - Extracts attractions, activities, and points of interest
  - Structured JSON output with titles, descriptions, images, and links
  - Anti-bot detection with custom headers
  
- **Booking.com Scraper** (`kaggle_booking_scraper.py`)
  - Extracts hotel listings with names, locations, prices, and star ratings
  - Dynamic price extraction
  - Structured hotel data in JSON format

### 2. LLM-Based Summarization ✓
- **Ollama Integration** (`llm_summarizer.py`)
  - Summarizes scraped attraction data
  - Summarizes hotel listings
  - Generates combined travel guides
  - Works offline with locally installed Ollama models
  - No API server needed

### 3. Data Storage ✓
- JSON-based data storage
- Structured outputs: `thrillophilia_pune_attractions.json`, `booking_hotels.json`
- Generated summaries: `thrillophilia_summary.txt`, `booking_summary.txt`, `combined_travel_guide.txt`

### 4. Live Weather Integration ✓
- **OpenWeatherMap API Integration** (`weather_service.py`)
  - Geocoding API to convert city names to coordinates
  - Current weather data (temperature, humidity, wind, visibility)
  - 5-day weather forecast with 3-hour intervals
  - Weather-based travel recommendations
  - Secure API key management with .env file
- **Example Usage** (`weather_example.py`)
  - Multiple city weather comparison
  - Travel planning weather checks
  - Forecast display and analysis

---

## 🚧 Features In Development (Roadmap)

### Phase 1: Enhance Web Scraping (In Progress)
### Phase 2: Personalized Itinerary Generator (Planned)
### Phase 3: Live Weather Integration ✅ COMPLETED
### Phase 4: Cost Prediction System (Planned)

---

## 📋 STEP-BY-STEP TO-DO LIST

### **PHASE 1: ENHANCE WEB SCRAPING SYSTEM** 🕷️

#### ✅ Completed Tasks
- [x] Create Thrillophilia scraper for attractions
- [x] Create Booking.com scraper for hotels
- [x] Implement JSON data storage
- [x] Add anti-bot headers
- [x] Extract star ratings from hotels

#### 🔲 Pending Tasks

**Task 1.1: Add More Data Sources**
- [ ] Create scraper for **Airbnb** (alternative accommodations)
  - File: `airbnb_scraper.py`
  - Extract: name, location, price per night, rating, amenities
- [ ] Create scraper for **Google Flights** or **Skyscanner** (flight prices)
  - File: `flight_scraper.py`
  - Extract: departure/arrival times, prices, airlines, duration
- [ ] Create scraper for **TripAdvisor** (reviews and ratings)
  - File: `tripadvisor_scraper.py`
  - Extract: reviews, ratings, tips
- [ ] Create scraper for **Zomato/Swiggy** (restaurant info)
  - File: `restaurant_scraper.py`
  - Extract: name, cuisine, price range, ratings
  - https://github.com/nikitperiwal/Zomato-Scraper/tree/master
  - https://github.com/DeevanshiSharma/Swiggy-Delhi-Top-Restaurants-Dataset-Scraped/blob/master/main_updated.ipynb

**Task 1.2: Improve Scraper Reliability**
- [ ] Add **error handling** for network failures
- [ ] Implement **retry mechanism** (3 attempts with exponential backoff)
- [ ] Add **logging system** to track scraping success/failures
  - File: `scraper_logger.py`
- [ ] Create **scraper scheduler** for periodic updates
  - File: `scheduler.py`
  - Use: `schedule` or `APScheduler` library

**Task 1.3: Handle Dynamic Content**
- [ ] Add **Selenium support** for JavaScript-heavy pages
  - Update existing scrapers or create: `selenium_scraper.py`
- [ ] Implement **wait strategies** for dynamic content loading
- [ ] Add **headless browser** option for faster scraping

**Task 1.4: Data Validation & Cleaning**
- [ ] Create **data validator** to check scraped data quality
  - File: `data_validator.py`
  - Check for: missing fields, invalid prices, broken links
- [ ] Implement **data cleaning** functions
  - Remove duplicates
  - Normalize price formats (₹, $, €)
  - Standardize date formats
- [ ] Add **data enrichment** (extract coordinates from addresses)

---

### **PHASE 2: PERSONALIZED ITINERARY GENERATOR** 🗓️

**Task 2.1: User Input System**
- [ ] Create **user input handler**
  - File: `user_input.py`
  - Collect: destination, budget, travel dates, group size, preferences
- [ ] Design **user preference questionnaire**
  - Travel style: adventure, relaxation, cultural, family-friendly
  - Interests: history, food, nature, shopping, nightlife
  - Mobility: walking distance preferences, accessibility needs
- [ ] Implement **budget category selection**
  - Budget: ₹0-10k/day
  - Mid-range: ₹10k-30k/day
  - Luxury: ₹30k+/day

**Task 2.2: Itinerary Generation Engine**
- [ ] Create **itinerary generator core**
  - File: `itinerary_generator.py`
  - Use scraped data + user preferences
- [ ] Implement **day-wise planning algorithm**
  - Morning, afternoon, evening activities
  - Optimize for location proximity (minimize travel time)
  - Balance activity types (mix of attractions, food, rest)
- [ ] Add **budget allocation** across itinerary
  - Distribute budget: accommodation (40%), food (30%), activities (20%), transport (10%)
- [ ] Create **LLM-based itinerary enhancement**
  - Use Ollama to make itinerary more personalized
  - Add contextual recommendations
  - Generate day summaries

**Task 2.3: Optimization & Constraints**
- [ ] Implement **time optimization**
  - Calculate travel time between locations
  - Ensure activities fit within operating hours
- [ ] Add **group size considerations**
  - Solo traveler vs family vs group recommendations
  - Suggest group-friendly activities
- [ ] Implement **seasonal recommendations**
  - Best time to visit attractions
  - Weather-based activity suggestions

**Task 2.4: Output & Formatting**
- [ ] Create **itinerary formatter**
  - File: `itinerary_formatter.py`
  - Formats: PDF, JSON, HTML, text
- [ ] Generate **daily schedules** with:
  - Time slots
  - Activity details
  - Estimated costs
  - Directions/maps links
- [ ] Add **export options**
  - Email itinerary
  - Download as PDF
  - Share link

---

### **PHASE 3: LIVE WEATHER INTEGRATION** 🌦️ ✅ COMPLETED

**Task 3.1: Weather API Integration** ✅
- [x] Choose weather API provider
  - Options: **OpenWeatherMap** (free tier), 
  **WeatherAPI**, **AccuWeather**

  - geocoding api: https://openweathermap.org/api/geocoding-api
  - openweather api: https://openweathermap.org/current
- [x] Create **weather service module**
  - File: `weather_service.py` ✅ Created
  - Functions: get_current_weather(), get_forecast(), get_coordinates()
- [x] Add API key management
  - File: `.env.example` ✅ Created
  - Library: `python-dotenv` ✅ Added

**Task 3.2: Weather Data Features** ✅
- [x] Fetch **current weather** for destination
  - Temperature, conditions, humidity, wind
- [x] Get **5-day forecast** (OpenWeatherMap free tier provides 5 days)
  - Min/max temperatures
  - Rain probability
  - Weather warnings
- [x] Implement **3-hour forecast intervals**
  - For detailed day planning

**Task 3.3: Weather-Based Recommendations** ✅
- [x] Create **activity recommender based on weather**
  - File: `weather_example.py` ✅ Created (includes travel_weather_check function)
  - Rainy day → indoor activities (museums, malls, restaurants)
  - Hot day → beaches, water parks, AC venues
  - Pleasant weather → outdoor activities, hiking, sightseeing
- [x] Add **weather alerts** to recommendations
  - Temperature-based suggestions
  - Rain alerts
  - Humidity warnings
- [x] Implement **packing suggestions**
  - Based on weather forecast
  - "Bring umbrella", "Pack sunscreen", etc.

**Task 3.4: Display & Integration** ✅
- [x] Add weather display formatting
  - print_current_weather() method
  - print_forecast() method
- [x] Create **weather data export**
  - JSON export functionality
  - Structured weather data format
- [x] Integration ready
  - Can be easily integrated with itinerary generator
  - Automatically adjust activities based on weather

---

### **PHASE 4: TRAVEL COST PREDICTION SYSTEM** 💰

**Task 4.1: Historical Data Collection**
- [ ] Create **cost database**
  - File: `cost_database.json` or use SQLite
  - Store: accommodation costs, activity costs, food costs, transport costs
- [ ] Implement **data collection from scrapers**
  - Store historical price data
  - Track price trends over time
- [ ] Add **manual cost data entry**
  - For items not scraped (local transport, misc expenses)

**Task 4.2: Cost Prediction Model**
- [ ] Create **cost calculator**
  - File: `cost_predictor.py`
  - Input: duration, group size, travel style, destination
- [ ] Implement **base cost calculation**
  - Accommodation: price × nights × rooms needed
  - Activities: average cost × number of activities
  - Food: per person per day × group size × days
  - Transport: flights + local transport estimate
- [ ] Add **group size adjustments**
  - Shared accommodation discounts
  - Group activity discounts
  - Per-person vs per-group costs

**Task 4.3: Travel Style Factors**
- [ ] Define **travel style multipliers**
  - Budget: 0.7x base cost
  - Mid-range: 1.0x base cost
  - Luxury: 2.0x base cost
- [ ] Implement **seasonal pricing**
  - Peak season: 1.5x cost
  - Off-season: 0.8x cost
- [ ] Add **destination-specific factors**
  - Metro cities: higher cost
  - Small towns: lower cost

**Task 4.4: ML-Based Enhancement (Advanced)**
- [ ] Collect training data
  - Historical prices
  - User feedback on actual costs
- [ ] Train **simple regression model**
  - Library: scikit-learn
  - Features: duration, group size, destination, season, style
  - Target: total cost
- [ ] Implement **price trend prediction**
  - Predict if prices will increase/decrease
  - Suggest best booking time

**Task 4.5: Cost Breakdown & Display**
- [ ] Create **detailed cost breakdown**
  - Category-wise costs (accommodation, food, etc.)
  - Day-wise budget allocation
- [ ] Add **budget vs actual tracking**
  - Compare predicted vs actual costs (post-trip)
- [ ] Implement **cost-saving suggestions**
  - "Book 2 months in advance to save ₹5000"
  - "Visit in October instead of December to save 30%"

---

### **PHASE 5: INTEGRATION & USER INTERFACE** 🖥️

**Task 5.1: Backend Integration**
- [ ] Create **main application controller**
  - File: `main.py`
  - Coordinates all modules
- [ ] Implement **data flow pipeline**
  - User input → Scraping → Weather → Cost prediction → Itinerary generation
- [ ] Add **caching system**
  - Cache scraped data for 24 hours
  - Reduce API calls

**Task 5.2: Command-Line Interface (CLI)**
- [ ] Create **interactive CLI**
  - File: `cli.py`
  - Library: `click` or `argparse`
- [ ] Add **menu-driven navigation**
  - 1. Scrape new data
  - 2. Generate itinerary
  - 3. Check weather
  - 4. Predict costs
  - 5. View saved itineraries
- [ ] Implement **progress indicators**
  - Loading bars for scraping
  - Status messages

**Task 5.3: Web Interface (Optional)**
- [ ] Choose framework
  - **Streamlit** (easiest, fastest)
  - Flask/FastAPI (more control)
  - Gradio (good for AI apps)
- [ ] Design **web UI pages**
  - Home page with input form
  - Results page with itinerary
  - Weather page
  - Cost estimation page
- [ ] Add **interactive features**
  - Edit itinerary
  - Swap activities
  - Adjust budget

**Task 5.4: Output & Export**
- [ ] Create **PDF generator**
  - Library: `reportlab` or `fpdf`
  - Include: itinerary, maps, weather, costs
- [ ] Add **map visualization**
  - Library: `folium` or Google Maps API
  - Show route on map
- [ ] Implement **share functionality**
  - Generate shareable links
  - Email itinerary

---

### **PHASE 6: TESTING & DEPLOYMENT** 🚀

**Task 6.1: Testing**
- [ ] Write **unit tests** for each module
  - File: `tests/` directory
  - Library: `pytest`
- [ ] Perform **integration testing**
  - Test end-to-end flow
- [ ] Add **error handling tests**
  - Network failures
  - Invalid inputs
  - API rate limits

**Task 6.2: Documentation**
- [ ] Write **API documentation**
  - Document all functions
  - Add docstrings
- [ ] Create **user guide**
  - File: `USER_GUIDE.md`
  - Step-by-step instructions
- [ ] Add **examples**
  - Sample itineraries
  - Example commands

**Task 6.3: Performance Optimization**
- [ ] Profile code for bottlenecks
- [ ] Implement **parallel scraping**
  - Use `concurrent.futures` or `asyncio`
- [ ] Optimize **LLM prompts**
  - Reduce token usage
  - Faster generation

**Task 6.4: Deployment**
- [ ] Containerize with **Docker**
  - File: `Dockerfile`
- [ ] Deploy to **cloud platform**
  - Options: Heroku, AWS, Google Cloud, Azure
- [ ] Set up **CI/CD pipeline**
  - GitHub Actions

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama installed locally ([Download](https://ollama.ai/download))
- OpenWeatherMap API key ([Get Free Key](https://openweathermap.org/api))

### Setup

```bash
# Clone repository
git clone https://github.com/SwayamChandak/accuraTraveller.git
cd accuraTraveller/accuraTraveller

# Install dependencies
pip install -r requirements.txt

# Install and setup Ollama
ollama pull llama3.2

# Setup Weather API
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Edit .env and add your OpenWeatherMap API key
# OPENWEATHER_API_KEY=your_actual_api_key_here

# Run weather service example
python weather_example.py

# Run the LLM summarizer
python llm_summarizer.py
```

---

## 🛠️ Technology Stack

### Current
- **Python 3.x** - Core language
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **Ollama** - LLM integration (offline)
- **OpenWeatherMap API** - Weather data
- **python-dotenv** - Environment variable management
- **JSON** - Data storage

### Planned
- **Selenium** - Dynamic content scraping
- **Scikit-learn** - Cost prediction ML
- **Streamlit/Flask** - Web interface
- **Folium** - Map visualization
- **ReportLab** - PDF generation
- **SQLite** - Database for cost history
- **APScheduler** - Task scheduling
- **Pytest** - Testing

---

## 📁 Project Structure

```
AccuraTraveller/
├── accuraTraveller/
│   ├── example_usage.py              # Thrillophilia scraper
│   ├── kaggle_booking_scraper.py     # Booking.com scraper
│   ├── llm_summarizer.py             # Ollama LLM integration
│   ├── weather_service.py            # ✅ Weather API service
│   ├── weather_example.py            # ✅ Weather usage examples
│   ├── requirements.txt              # Dependencies
│   ├── .env.example                  # ✅ API key template
│   ├── .gitignore                    # ✅ Protect sensitive files
│   ├── thrillophilia_pune_attractions.json
│   ├── booking_hotels.json
│   ├── combined_travel_guide.txt
│   │
│   ├── zomato/                       # 🔄 In Progress
│   │   ├── info_scraper.py           # Restaurant info
│   │   ├── menu_scraper.py           # Menu details
│   │   └── review_scraper.py         # Reviews
│   │
│   ├── [TO BE CREATED]
│   ├── airbnb_scraper.py             # Phase 1
│   ├── flight_scraper.py             # Phase 1
│   ├── cost_predictor.py             # Phase 4
│   ├── itinerary_generator.py        # Phase 2
│   ├── main.py                       # Phase 5
│   └── cli.py                        # Phase 5
│
└── README.md
```

---

## 🎯 Quick Start Guide

### Current Usage

1. **Scrape Attractions (Thrillophilia)**
```bash
python example_usage.py
```

2. **Scrape Hotels (Booking.com)**
```bash
python kaggle_booking_scraper.py
```

3. **Check Weather for Travel Destination**
```bash
# Setup API key first (see Installation section)
python weather_example.py
```

4. **Generate Travel Summary with LLM**
```bash
python llm_summarizer.py
# Choose option 3 for combined travel guide
```

### API Usage Examples

**Weather Service:**
```python
from weather_service import WeatherService

# Initialize
weather = WeatherService(api_key="your_api_key")

# Get current weather
data = weather.get_weather_by_city("Mumbai")
weather.print_current_weather(data)

# Get 5-day forecast
forecast = weather.get_forecast_by_city("Goa", days=3)
weather.print_forecast(forecast)
```

### Future Usage (After Phase 5)

```bash
python main.py
# Interactive menu will guide you through:
# 1. Enter destination and preferences
# 2. Generate personalized itinerary
# 3. View weather forecast
# 4. Get cost estimation
# 5. Export itinerary as PDF
```

---

## 🤝 Contributing

This is an active development project. Contributions are welcome!

### Priority Areas
1. Adding new scrapers (Airbnb, Flights, etc.)
2. ~~Weather API integration~~ ✅ DONE
3. Cost prediction algorithm
4. UI/UX improvements
5. Personalized itinerary generation

---

## 📊 Progress Tracker

| Phase | Feature | Status | Priority |
|-------|---------|--------|----------|
| 1 | Web Scraping (Basic) | ✅ Done | - |
| 1 | Add More Scrapers | � In Progress | High |
| 1 | Selenium Support | 🔲 To Do | Medium |
| 2 | User Input System | 🔲 To Do | High |
| 2 | Itinerary Generator | 🔲 To Do | High |
| 2 | Budget Allocation | 🔲 To Do | High |
| 3 | Weather API | ✅ Done | - |
| 3 | Weather Recommendations | ✅ Done | - |
| 3 | Geocoding Service | ✅ Done | - |
| 3 | Forecast Display | ✅ Done | - |
| 4 | Cost Database | 🔲 To Do | High |
| 4 | Cost Predictor | 🔲 To Do | High |
| 4 | ML Model | 🔲 To Do | Low |
| 5 | CLI Interface | 🔲 To Do | Medium |
| 5 | Web Interface | 🔲 To Do | Low |
| 5 | PDF Export | 🔲 To Do | Medium |

---

## 📝 License

Educational project. Use responsibly and ethically.

---

## 📧 Contact

**Developer:** Swayam Chandak  
**GitHub:** [@SwayamChandak](https://github.com/SwayamChandak)  
**Repository:** [AccuraTraveller](https://github.com/SwayamChandak/accuraTraveller)

---

## 🙏 Acknowledgments

- BeautifulSoup4 for HTML parsing
- Ollama for local LLM capabilities
- Open-source community for various libraries

---

**Last Updated:** November 11, 2025  
**Version:** 0.1.0 (Early Development)
