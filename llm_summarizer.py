"""
JSON Summary Generator using Ollama LLM
Generates intelligent summaries of scraped travel data from JSON files
Uses Ollama Python library - no API server needed!
"""

import json
import ollama


class OllamaSummarizer:
    """
    Summarize JSON data using Ollama LLM.
    Works directly with locally installed Ollama models.
    No server needed!
    """
    
    def __init__(self, model="llama3.2"):
        """
        Initialize the Ollama summarizer.
        
        Args:
            model: Ollama model to use (default: llama3.2)
        """
        self.model = model
        print(f"Using Ollama model: {self.model}")
    
    def load_json(self, file_path):
        """Load JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{file_path}'")
            return None
    
    def generate_summary(self, prompt):
        """
        Generate summary using Ollama.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            Generated summary text
        """
        try:
            print(f"Generating summary with {self.model}...")
            print("(This may take a moment...)\n")
            
            # Use Ollama's generate function directly
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            
            return response['response']
                
        except Exception as e:
            print(f"\n⚠️  Error generating summary: {e}")
            print("\nMake sure:")
            print(f"1. Ollama is installed")
            print(f"2. Model '{self.model}' is downloaded: ollama pull {self.model}")
            return None
    
    def summarize_thrillophilia_data(self, json_file):
        """
        Summarize Thrillophilia attractions data.
        
        Args:
            json_file: Path to thrillophilia JSON file
            
        Returns:
            Summary text
        """
        data = self.load_json(json_file)
        if not data:
            return None
        
        # Create a concise prompt for the LLM
        attractions_list = []
        for attraction in data.get('attractions', [])[:15]:  # Limit to first 15 to avoid token limits
            title = attraction.get('title', 'N/A')
            content = attraction.get('content', {})
            full_text = content.get('full_text', '')[:200] if isinstance(content, dict) else str(content)[:200]
            attractions_list.append(f"- {title}: {full_text}")
        
        prompt = f"""You are a travel expert. Analyze this data about things to do in a city and provide a comprehensive summary.

Title: {data.get('page_title', 'N/A')}
Total Attractions: {data.get('total_attractions', 0)}
Scraped: {data.get('scraped_at', 'N/A')}

Top Attractions:
{chr(10).join(attractions_list)}

Please provide:
1. A brief overview of the destination
2. Top 5 must-visit attractions with brief descriptions
3. Types of activities available (adventure, cultural, historical, etc.)
4. Best suited for which type of travelers
5. Key highlights and unique experiences

Keep the summary concise and informative (around 300-400 words)."""

        return self.generate_summary(prompt)
    
    def summarize_booking_data(self, json_file):
        """
        Summarize Booking.com hotels data.
        
        Args:
            json_file: Path to booking JSON file
            
        Returns:
            Summary text
        """
        data = self.load_json(json_file)
        if not data:
            return None
        
        # Analyze hotel data
        hotels = data.get('hotels', [])
        total_hotels = len(hotels)
        
        # Extract ratings (only valid ones)
        ratings = [h.get('rating', 'N/A') for h in hotels if h.get('rating') != 'N/A']
        
        # Sample hotels for summary
        sample_hotels = []
        for hotel in hotels[:10]:  # First 10 hotels
            name = hotel.get('name', 'N/A')
            location = hotel.get('location', 'N/A')
            price = hotel.get('price', 'N/A')
            rating = hotel.get('rating', 'N/A')
            sample_hotels.append(f"- {name} | Location: {location} | Price: {price} | Rating: {rating}")
        
        prompt = f"""You are a travel accommodation expert. Analyze this hotel booking data and provide a helpful summary.

Search URL: {data.get('search_url', 'N/A')}
Total Hotels Found: {total_hotels}
Scraped: {data.get('scraped_at', 'N/A')}

Sample Hotels:
{chr(10).join(sample_hotels)}

Please provide:
1. Overview of accommodation options in this area
2. Price range analysis (budget, mid-range, luxury)
3. Top 3-5 recommended hotels with reasons
4. Popular areas/neighborhoods mentioned
5. General recommendations for travelers

Keep the summary practical and informative (around 300-400 words)."""

        return self.generate_summary(prompt)
    
    def compare_both_datasets(self, thrillophilia_file, booking_file):
        """
        Generate a combined travel guide summary from both datasets.
        
        Args:
            thrillophilia_file: Path to thrillophilia JSON
            booking_file: Path to booking JSON
            
        Returns:
            Combined summary
        """
        thrillophilia_data = self.load_json(thrillophilia_file)
        booking_data = self.load_json(booking_file)
        
        if not thrillophilia_data or not booking_data:
            print("Error: Could not load one or both JSON files")
            return None
        
        # Prepare combined data
        attractions = thrillophilia_data.get('attractions', [])[:10]
        hotels = booking_data.get('hotels', [])[:8]
        
        attractions_text = "\n".join([
            f"{i+1}. {a.get('title', 'N/A')}" 
            for i, a in enumerate(attractions)
        ])
        
        hotels_text = "\n".join([
            f"{i+1}. {h.get('name', 'N/A')} - {h.get('location', 'N/A')} - {h.get('rating', 'N/A')}" 
            for i, h in enumerate(hotels)
        ])
        
        prompt = f"""You are an expert travel planner. Create a comprehensive travel guide combining attractions and accommodation data.

ATTRACTIONS DATA:
Total Things to Do: {thrillophilia_data.get('total_attractions', 0)}
Top Attractions:
{attractions_text}

ACCOMMODATION DATA:
Total Hotels Available: {len(booking_data.get('hotels', []))}
Sample Hotels:
{hotels_text}

Please create a complete travel guide that includes:
1. Destination Overview
2. Top 5 Must-Do Activities (from attractions data)
3. Recommended Hotels (from booking data)
4. Suggested Itinerary (2-3 days)
5. Budget Estimates
6. Best Time to Visit
7. Travel Tips

Make it practical, engaging, and ready for travelers to use. Around 500-600 words."""

        return self.generate_summary(prompt)
    
    def save_summary(self, summary, output_file):
        """Save summary to a text file."""
        if summary:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"\n✅ Summary saved to '{output_file}'")


def main():
    """Main function to generate summaries."""
    print("=" * 60)
    print("JSON Summary Generator using Ollama LLM")
    print("=" * 60)
    
    # Initialize summarizer
    summarizer = OllamaSummarizer(model="llama3.2")  # Change model as needed
    
    # File paths
    thrillophilia_file = 'thrillophilia_pune_attractions.json'
    booking_file = 'booking_hotels.json'
    
    print("\n📋 Choose summary type:")
    print("1. Summarize Thrillophilia attractions only")
    print("2. Summarize Booking.com hotels only")
    print("3. Generate combined travel guide (RECOMMENDED)")
    print("4. Generate all summaries")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        print("\n" + "="*60)
        print("THRILLOPHILIA ATTRACTIONS SUMMARY")
        print("="*60 + "\n")
        summary = summarizer.summarize_thrillophilia_data(thrillophilia_file)
        if summary:
            print("\n" + summary)
            summarizer.save_summary(summary, 'thrillophilia_summary.txt')
    
    elif choice == '2':
        print("\n" + "="*60)
        print("BOOKING.COM HOTELS SUMMARY")
        print("="*60 + "\n")
        summary = summarizer.summarize_booking_data(booking_file)
        if summary:
            print("\n" + summary)
            summarizer.save_summary(summary, 'booking_summary.txt')
    
    elif choice == '3':
        print("\n" + "="*60)
        print("COMBINED TRAVEL GUIDE")
        print("="*60 + "\n")
        summary = summarizer.compare_both_datasets(thrillophilia_file, booking_file)
        if summary:
            print("\n" + summary)
            summarizer.save_summary(summary, 'combined_travel_guide.txt')
    
    elif choice == '4':
        print("\n📝 Generating all summaries...\n")
        
        # 1. Thrillophilia summary
        print("="*60)
        print("1. THRILLOPHILIA ATTRACTIONS SUMMARY")
        print("="*60 + "\n")
        summary1 = summarizer.summarize_thrillophilia_data(thrillophilia_file)
        if summary1:
            print("\n" + summary1)
            summarizer.save_summary(summary1, 'thrillophilia_summary.txt')
        
        # 2. Booking summary
        print("\n" + "="*60)
        print("2. BOOKING.COM HOTELS SUMMARY")
        print("="*60 + "\n")
        summary2 = summarizer.summarize_booking_data(booking_file)
        if summary2:
            print("\n" + summary2)
            summarizer.save_summary(summary2, 'booking_summary.txt')
        
        # 3. Combined guide
        print("\n" + "="*60)
        print("3. COMBINED TRAVEL GUIDE")
        print("="*60 + "\n")
        summary3 = summarizer.compare_both_datasets(thrillophilia_file, booking_file)
        if summary3:
            print("\n" + summary3)
            summarizer.save_summary(summary3, 'combined_travel_guide.txt')
        
        print("\n" + "="*60)
        print("✅ All summaries generated successfully!")
        print("="*60)
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    print("\n⚠️  PREREQUISITES:")
    print("1. Install Ollama: https://ollama.ai/download")
    print("2. Pull a model: ollama pull llama3.2")
    print("3. Install Python package: pip install ollama")
    print("4. Make sure JSON files exist in the current directory")
    print("\nNOTE: No Ollama server needed! Works directly with installed models.\n")
    
    main()
