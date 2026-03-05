import requests
from typing import Dict, Optional
from datetime import datetime

class AQISearch:
    """
    Search module for location-based AQI queries
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.aqi_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    
    def geocode_location(self, query: str) -> Optional[Dict]:
        """
        Convert location name to coordinates
        """
        try:
            params = {
                'q': query,
                'appid': self.api_key,
                'limit': 1
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data:
                return {
                    'city': data[0].get('name'),
                    'country': data[0].get('country'),
                    'lat': data[0].get('lat'),
                    'lon': data[0].get('lon')
                }
            return None
        except Exception as e:
            return {'error': str(e)}
    
    def fetch_aqi(self, lat: float, lon: float) -> Dict:
        """
        Fetch AQI data for given coordinates
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            response = requests.get(self.aqi_url, params=params, timeout=10)
            data = response.json()
            
            if 'list' in data and data['list']:
                components = data['list'][0].get('components', {})
                return {
                    'pm2_5': components.get('pm2_5'),
                    'pm10': components.get('pm10'),
                    'no2': components.get('no2'),
                    'so2': components.get('so2'),
                    'o3': components.get('o3'),
                    'co': components.get('co'),
                    'timestamp': datetime.now().isoformat()
                }
            return {'error': 'No data available'}
        except Exception as e:
            return {'error': str(e)}
    
    def search(self, location: str) -> Dict:
        """
        Complete search - geocode then fetch AQI
        """
        geo_data = self.geocode_location(location)
        
        if not geo_data or 'error' in geo_data:
            return geo_data
        
        aqi_data = self.fetch_aqi(geo_data['lat'], geo_data['lon'])
        
        return {
            'location': geo_data,
            'aqi_data': aqi_data
        }
