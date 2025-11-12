# Weather Service - Quick Usage Guide

## Setup

### 1. Get API Key
1. Go to https://openweathermap.org/api
2. Click "Sign Up" (it's free!)
3. After signing up, go to "API Keys" section
4. Copy your API key

### 2. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your key
# Change: OPENWEATHER_API_KEY=your_api_key_here
# To: OPENWEATHER_API_KEY=abc123your_actual_key_here
```

Or set environment variable directly:
```powershell
# Windows PowerShell
$env:OPENWEATHER_API_KEY='your_actual_key_here'
```

```bash
# Linux/Mac
export OPENWEATHER_API_KEY='your_actual_key_here'
```

### 3. Install Dependencies
```bash
pip install requests python-dotenv
```

## Basic Usage

### Method 1: Using the Example Script
```bash
python weather_example.py
```

This will show:
- Multiple city searches
- Current weather for Mumbai
- Weather by coordinates (Pune)
- 3-day forecast for Goa
- Multi-city comparison
- Travel weather recommendations

### Method 2: In Your Own Code

```python
from weather_service import WeatherService

# Initialize
weather = WeatherService(api_key="your_key")

# Get current weather for a city
data = weather.get_weather_by_city("London")
weather.print_current_weather(data)
```

## Common Use Cases

### 1. Check Weather Before Travel
```python
from weather_service import WeatherService

weather = WeatherService()

# Check current weather
current = weather.get_weather_by_city("Goa,IN")
print(f"Temperature: {current['temperature']['current']}°C")
print(f"Weather: {current['weather']['description']}")

# Get forecast
forecast = weather.get_forecast_by_city("Goa,IN", days=3)
weather.print_forecast(forecast)
```

### 2. Compare Multiple Destinations
```python
from weather_service import WeatherService

weather = WeatherService()

cities = ["Mumbai,IN", "Goa,IN", "Bangalore,IN"]

for city in cities:
    data = weather.get_weather_by_city(city)
    print(f"{data['location']}: {data['temperature']['current']}°C, {data['weather']['description']}")
```

### 3. Get Weather by Coordinates
```python
from weather_service import WeatherService

weather = WeatherService()

# If you have lat/lon coordinates
lat, lon = 18.5204, 73.8567  # Pune
data = weather.get_weather(lat, lon)
weather.print_current_weather(data)
```

### 4. Search for Cities
```python
from weather_service import WeatherService

weather = WeatherService()

# Find all places named "London"
locations = weather.get_coordinates("London", limit=5)

for loc in locations:
    print(f"{loc['name']}, {loc['country']} - {loc['lat']}, {loc['lon']}")
```

### 5. Save Weather Data
```python
from weather_service import WeatherService

weather = WeatherService()

data = weather.get_weather_by_city("Paris,FR")
weather.save_weather_data(data, "paris_weather.json")
```

## Available Methods

### WeatherService Class

**`get_coordinates(city, limit=5)`**
- Get lat/lon for a city name
- Returns list of matching locations
- Example: `weather.get_coordinates("London")`

**`get_weather(lat, lon, units='metric')`**
- Get current weather by coordinates
- Units: 'metric' (°C), 'imperial' (°F), 'standard' (K)
- Example: `weather.get_weather(51.5074, -0.1278)`

**`get_weather_by_city(city, units='metric')`**
- Get current weather by city name
- Easiest method - combines geocoding + weather
- Example: `weather.get_weather_by_city("Tokyo,JP")`

**`get_forecast(lat, lon, units='metric', days=5)`**
- Get forecast by coordinates
- Max 5 days (free API tier)
- Example: `weather.get_forecast(51.5074, -0.1278, days=3)`

**`get_forecast_by_city(city, units='metric', days=5)`**
- Get forecast by city name
- Example: `weather.get_forecast_by_city("London", days=3)`

**`print_current_weather(weather_data)`**
- Pretty print weather data
- Example: `weather.print_current_weather(data)`

**`print_forecast(forecast_data, days_to_show=3)`**
- Pretty print forecast
- Example: `weather.print_forecast(forecast, days_to_show=3)`

**`save_weather_data(weather_data, filename)`**
- Save to JSON file
- Example: `weather.save_weather_data(data, "weather.json")`

## Data Structure

### Current Weather Data
```python
{
    'location': 'London',
    'country': 'GB',
    'coordinates': {'lat': 51.5074, 'lon': -0.1278},
    'temperature': {
        'current': 15.2,
        'feels_like': 14.5,
        'min': 13.0,
        'max': 17.0,
        'unit': '°C'
    },
    'weather': {
        'main': 'Clouds',
        'description': 'overcast clouds',
        'icon': '04d'
    },
    'wind': {
        'speed': 5.5,
        'deg': 270,
        'unit': 'm/s'
    },
    'humidity': 75,
    'pressure': 1013,
    'visibility': 10.0,
    'clouds': 90,
    'sunrise': '06:30:15',
    'sunset': '18:45:30',
    'timestamp': '2025-11-12 14:30:00'
}
```

### Forecast Data
```python
{
    'location': 'London',
    'country': 'GB',
    'coordinates': {'lat': 51.5074, 'lon': -0.1278},
    'unit': '°C',
    'forecast': [
        {
            'datetime': '2025-11-12 15:00:00',
            'date': '2025-11-12',
            'time': '15:00',
            'temp': 15.5,
            'feels_like': 14.8,
            'temp_min': 14.0,
            'temp_max': 16.0,
            'weather': 'Clouds',
            'description': 'overcast clouds',
            'humidity': 72,
            'wind_speed': 5.2,
            'rain_probability': 20.0
        },
        # ... more forecast entries
    ]
}
```

## Error Handling

```python
from weather_service import WeatherService

try:
    weather = WeatherService(api_key="your_key")
    data = weather.get_weather_by_city("InvalidCity12345")
    
    if data:
        weather.print_current_weather(data)
    else:
        print("City not found or error occurred")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Tips

1. **City Names**: Use format "City,Country" for better accuracy
   - Good: "London,UK", "Paris,FR", "Mumbai,IN"
   - Also works: "London" (but may return multiple results)

2. **API Rate Limits**: Free tier allows 60 calls/minute, 1,000,000 calls/month

3. **Caching**: Consider caching weather data for a few hours to reduce API calls

4. **Units**: 
   - `metric` → °C, m/s
   - `imperial` → °F, mph
   - `standard` → K, m/s

5. **Coordinates**: If you have exact coordinates, use `get_weather()` directly for faster results

## Troubleshooting

**"API key is required" error:**
- Make sure .env file exists and has correct key
- Or set environment variable
- Or pass key directly: `WeatherService(api_key="your_key")`

**"No results found for city":**
- Check spelling
- Try adding country code: "Mumbai,IN"
- Use `get_coordinates()` first to see available options

**Connection errors:**
- Check internet connection
- Verify API key is active (may take a few minutes after signup)
- Check OpenWeatherMap service status

**Import errors:**
- Install required packages: `pip install requests python-dotenv`

## Integration with Travel Planning

```python
from weather_service import WeatherService

def plan_trip(destination, days):
    weather = WeatherService()
    
    # Get current weather
    current = weather.get_weather_by_city(destination)
    
    # Get forecast
    forecast = weather.get_forecast_by_city(destination, days=days)
    
    # Analyze and recommend
    temps = [f['temp'] for f in forecast['forecast']]
    avg_temp = sum(temps) / len(temps)
    
    print(f"\n🌍 Trip Planning for {destination}")
    print(f"📅 Duration: {days} days")
    print(f"🌡️  Average Temperature: {avg_temp:.1f}°C")
    
    if avg_temp > 30:
        print("🏖️  Beach wear, sunscreen, light clothes")
    elif avg_temp < 15:
        print("🧥 Warm clothes, jackets, sweaters")
    else:
        print("👕 Comfortable casual wear")
    
    # Check for rain
    rain_days = [f for f in forecast['forecast'] if 'rain' in f['description'].lower()]
    if rain_days:
        print(f"🌧️  Rain expected on {len(rain_days)} days - pack umbrella!")

# Use it
plan_trip("Goa,IN", 5)
```

## Next Steps

- Integrate with your itinerary generator
- Add weather-based activity recommendations
- Create weather alerts for travel days
- Build a weather dashboard

For more examples, see `weather_example.py`!
