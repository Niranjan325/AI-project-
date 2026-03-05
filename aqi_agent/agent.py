import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AQIAgent:
    """
    Autonomous Air Quality Index Agent
    - Monitors air quality in real-time
    - Provides intelligent recommendations
    - Handles location-based queries
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.search_history = []
        self.alerts = []
        self.base_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    
    def search_location_aqi(self, city: str, country: str = None) -> Dict:
        """
        Search and fetch AQI for a specific location
        """
        try:
            # Geocode the location
            geocoding_url = f"https://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': f"{city},{country}" if country else city,
                'appid': self.api_key,
                'limit': 1
            }
            
            geo_response = requests.get(geocoding_url, params=params, timeout=10)
            geo_data = geo_response.json()
            
            if not geo_data:
                return {'error': 'Location not found'}
            
            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
            
            # Fetch AQI data
            aqi_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            aqi_response = requests.get(self.base_url, params=aqi_params, timeout=10)
            aqi_data = aqi_response.json()
            
            pollutants = aqi_data.get('list', [{}])[0].get('components', {})
            
            result = {
                'location': city,
                'country': country,
                'coordinates': {'lat': lat, 'lon': lon},
                'timestamp': datetime.now().isoformat(),
                'pollutants': pollutants,
                'main_pollutant': max(pollutants.items(), key=lambda x: x[1])[0] if pollutants else None
            }
            
            # Log search history
            self.search_history.append(result)
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_health_alert(self, aqi_value: float) -> str:
        """
        Generate health alerts based on AQI value
        """
        if aqi_value <= 50:
            return "✅ Good - Outdoor activities are safe"
        elif aqi_value <= 100:
            return "🟡 Satisfactory - Acceptable air quality"
        elif aqi_value <= 150:
            return "🟠 Moderate - Sensitive groups should limit outdoor activities"
        elif aqi_value <= 200:
            return "🔴 Poor - Avoid outdoor activities, use N95 masks"
        else:
            return "⚠️ Severe - Stay indoors, dangerous pollution levels"
    
    def analyze_trend(self) -> Dict:
        """
        Analyze air quality trends from search history
        """
        if len(self.search_history) < 2:
            return {'message': 'Insufficient data for trend analysis'}
        
        locations = {}
        for record in self.search_history:
            city = record['location']
            if city not in locations:
                locations[city] = []
            locations[city].append(record)
        
        return {
            'total_searches': len(self.search_history),
            'unique_locations': len(locations),
            'locations_data': locations
        }
    
    def set_alert(self, location: str, threshold: float) -> Dict:
        """
        Set alert for specific location when AQI exceeds threshold
        """
        alert = {
            'location': location,
            'threshold': threshold,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        self.alerts.append(alert)
        return {'status': 'Alert set', 'alert': alert}
    
    def get_search_history(self) -> List[Dict]:
        """
        Retrieve search history
        """
        return self.search_history
    
    def export_data(self, filename: str = 'aqi_data.json') -> str:
        """
        Export collected data to JSON file
        """
        data = {
            'search_history': self.search_history,
            'alerts': self.alerts,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"Data exported to {filename}"


if __name__ == "__main__":
    # Example usage
    agent = AQIAgent()
    
    # Test location search
    print("🔍 Searching AQI for New Delhi...")
    result = agent.search_location_aqi("New Delhi", "IN")
    print(json.dumps(result, indent=2))
