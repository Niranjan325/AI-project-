import requests
import json
from datetime import datetime
from typing import Dict, Tuple

class AQIMonitor:
    """
    Air Quality Index Monitor
    Fetches and calculates air quality data based on pollutant concentrations
    """
    
    # AQI Breakpoints for different pollutants (US EPA Standards)
    AQI_BREAKPOINTS = {
        'PM2.5': [
            (0, 12, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 500, 301, 500)
        ],
        'PM10': [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 604, 301, 500)
        ],
        'O3': [
            (0, 54, 0, 50),
            (55, 70, 51, 100),
            (71, 85, 101, 150),
            (86, 105, 151, 200),
            (106, 200, 201, 300),
            (201, 2000, 301, 500)
        ],
        'NO2': [
            (0, 53, 0, 50),
            (54, 100, 51, 100),
            (101, 360, 101, 150),
            (361, 649, 151, 200),
            (650, 1249, 201, 300),
            (1250, 2049, 301, 500)
        ],
        'SO2': [
            (0, 35, 0, 50),
            (36, 75, 51, 100),
            (76, 185, 101, 150),
            (186, 304, 151, 200),
            (305, 604, 201, 300),
            (605, 1004, 301, 500)
        ]
    }
    
    AQI_CATEGORIES = {
        'Good': (0, 50),
        'Satisfactory': (51, 100),
        'Moderately Polluted': (101, 150),
        'Poor': (151, 200),
        'Very Poor': (201, 300),
        'Severe': (301, 500)
    }
    
    def __init__(self, api_key: str = None):
        """Initialize AQI Monitor with optional API key"""
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    
    def calculate_aqi_from_pollutants(self, pollutants: Dict) -> Tuple[float, str]:
        """
        Calculate AQI based on pollutant concentrations
        Returns: (aqi_value, category)
        """
        max_aqi = 0
        dominant_pollutant = None
        
        for pollutant, value in pollutants.items():
            if pollutant not in self.AQI_BREAKPOINTS:
                continue
            
            aqi = self._calculate_pollutant_aqi(pollutant, value)
            if aqi > max_aqi:
                max_aqi = aqi
                dominant_pollutant = pollutant
        
        category = self._get_aqi_category(max_aqi)
        return max_aqi, category, dominant_pollutant
    
    def _calculate_pollutant_aqi(self, pollutant: str, concentration: float) -> float:
        """
        Calculate AQI for a specific pollutant using breakpoint method
        """
        breakpoints = self.AQI_BREAKPOINTS[pollutant]
        
        for bp_low, bp_high, aqi_low, aqi_high in breakpoints:
            if bp_low <= concentration <= bp_high:
                # Linear interpolation
                aqi = ((aqi_high - aqi_low) / (bp_high - bp_low)) * (concentration - bp_low) + aqi_low
                return round(aqi, 2)
        
        # If concentration exceeds highest breakpoint
        return 500
    
    def _get_aqi_category(self, aqi_value: float) -> str:
        """
        Get AQI category based on value
        """
        for category, (low, high) in self.AQI_CATEGORIES.items():
            if low <= aqi_value <= high:
                return category
        return 'Severe'
    
    def get_aqi_by_location(self, lat: float, lon: float) -> Dict:
        """
        Fetch air quality data for specific coordinates
        Requires OpenWeatherMap API key
        """
        if not self.api_key:
            return {"error": "API key not provided"}
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pollutants = data.get('list', [{}])[0].get('components', {})
            
            aqi_value, category, dominant = self.calculate_aqi_from_pollutants(pollutants)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'location': {'lat': lat, 'lon': lon},
                'aqi': aqi_value,
                'category': category,
                'dominant_pollutant': dominant,
                'pollutants': pollutants
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_health_recommendation(self, aqi_value: float) -> str:
        """
        Provide health recommendations based on AQI value
        """
        recommendations = {
            'Good': 'Air quality is satisfactory. Outdoor activities are recommended.',
            'Satisfactory': 'Air quality is acceptable. Outdoor activities are safe.',
            'Moderately Polluted': 'Sensitive groups should limit outdoor activities.',
            'Poor': 'Avoid outdoor activities. Use N95 masks if going outside.',
            'Very Poor': 'Stay indoors. Use air purifiers and N95 masks outside.',
            'Severe': 'Dangerous levels. Avoid outdoor activities completely.'
        }
        
        category = self._get_aqi_category(aqi_value)
        return recommendations.get(category, 'Unknown')


if __name__ == "__main__":
    # Example usage
    monitor = AQIMonitor()
    
    # Test with sample pollutant data
    sample_pollutants = {
        'PM2.5': 25.5,
        'PM10': 45.2,
        'O3': 60.0,
        'NO2': 80.5,
        'SO2': 50.0
    }
    
    aqi, category, dominant = monitor.calculate_aqi_from_pollutants(sample_pollutants)
    print(f"AQI: {aqi}")
    print(f"Category: {category}")
    print(f"Dominant Pollutant: {dominant}")
    print(f"Health Recommendation: {monitor.get_health_recommendation(aqi)}")
