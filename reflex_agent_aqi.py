import json
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum

class AQILevel(Enum):
    """AQI Level Classification"""
    GOOD = (0, 50, "Good")
    SATISFACTORY = (51, 100, "Satisfactory")
    MODERATELY_POLLUTED = (101, 150, "Moderately Polluted")
    POOR = (151, 200, "Poor")
    VERY_POOR = (201, 300, "Very Poor")
    SEVERE = (301, 500, "Severe")

class EnvironmentalSensor:
    """Simulates environmental sensors reading pollutant data"""
    
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        self.last_reading = None
    
    def read_sensors(self, data: Dict) -> Dict:
        """Read sensor data from file"""
        return {
            'pm2_5': data.get('pm2_5', 0),
            'pm10': data.get('pm10', 0),
            'no2': data.get('no2', 0),
            'so2': data.get('so2', 0),
            'o3': data.get('o3', 0),
            'timestamp': datetime.now().isoformat()
        }

class AQIReflexAgent:
    """
    Simple Reflex Agent for Environmental AQI Monitoring
    
    Agent Architecture:
    Sensors -> Percepts -> Decision Rules -> Actions
    
    The agent:
    1. Reads environmental data from sensors
    2. Calculates AQI based on pollutant concentrations
    3. Generates immediate responses (reflexes) without internal state
    4. Recommends health actions
    """
    
    def __init__(self):
        self.sensor = EnvironmentalSensor("aqi_sensor_001")
        self.aqi_rules = self._initialize_rules()
        self.action_map = self._initialize_actions()
    
    def _initialize_rules(self) -> Dict:
        """Define condition-action rules for reflexive behavior"""
        return {
            'high_pm25': lambda pm: pm > 100,
            'high_pm10': lambda pm: pm > 150,
            'high_no2': lambda no2: no2 > 200,
            'high_so2': lambda so2: so2 > 100,
            'high_o3': lambda o3: o3 > 120
        }
    
    def _initialize_actions(self) -> Dict:
        """Define reflex actions for different AQI conditions"""
        return {
            'GOOD': 'Outdoor activities are safe. No precautions needed.',
            'SATISFACTORY': 'Air quality is acceptable. Children and elderly should limit activities.',
            'MODERATELY_POLLUTED': 'Sensitive groups should avoid outdoor activities.',
            'POOR': 'ALERT: Avoid outdoor activities. Use N95 masks. Stay indoors if possible.',
            'VERY_POOR': 'WARNING: Hazardous. Stay indoors. Use air purifiers. Wear N95 masks.',
            'SEVERE': 'CRITICAL: Emergency alert. Avoid all outdoor activities. Seek emergency care if experiencing symptoms.'
        }
    
    def perceive(self, sensor_data: Dict) -> Dict:
        """
        Perceive environmental conditions from sensors
        This is the perception phase of the reflex agent
        """
        return self.sensor.read_sensors(sensor_data)
    
    def calculate_aqi(self, percepts: Dict) -> float:
        """
        Calculate AQI using EPA breakpoint method
        Returns: AQI value (0-500)
        """
        # Simplified AQI calculation based on PM2.5
        pm25 = percepts.get('pm2_5', 0)
        
        if pm25 <= 12:
            aqi = (pm25 / 12) * 50
        elif pm25 <= 35.4:
            aqi = ((pm25 - 12) / (35.4 - 12)) * (100 - 50) + 50
        elif pm25 <= 55.4:
            aqi = ((pm25 - 35.4) / (55.4 - 35.4)) * (150 - 100) + 100
        elif pm25 <= 150.4:
            aqi = ((pm25 - 55.4) / (150.4 - 55.4)) * (200 - 150) + 150
        elif pm25 <= 250.4:
            aqi = ((pm25 - 150.4) / (250.4 - 150.4)) * (300 - 200) + 200
        else:
            aqi = 500
        
        return round(aqi, 2)
    
    def get_aqi_level(self, aqi: float) -> str:
        """Determine AQI level from numeric value"""
        for level in AQILevel:
            if level.value[0] <= aqi <= level.value[1]:
                return level.name
        return "SEVERE"
    
    def apply_rules(self, percepts: Dict) -> List[str]:
        """
        Apply if-then rules to generate immediate responses
        This demonstrates the rule-based reflex behavior
        """
        triggered_alerts = []
        
        if self.aqi_rules['high_pm25'](percepts.get('pm2_5', 0)):
            triggered_alerts.append("High PM2.5 detected")
        
        if self.aqi_rules['high_pm10'](percepts.get('pm10', 0)):
            triggered_alerts.append("High PM10 detected")
        
        if self.aqi_rules['high_no2'](percepts.get('no2', 0)):
            triggered_alerts.append("High NO2 detected")
        
        if self.aqi_rules['high_so2'](percepts.get('so2', 0)):
            triggered_alerts.append("High SO2 detected")
        
        if self.aqi_rules['high_o3'](percepts.get('o3', 0)):
            triggered_alerts.append("High O3 detected")
        
        return triggered_alerts
    
    def act(self, aqi_level: str) -> str:
        """
        Execute immediate action based on AQI level
        This is the action phase with no internal state memory
        """
        return self.action_map.get(aqi_level, "Unknown AQI level")
    
    def react_to_environment(self, sensor_data: Dict) -> Dict:
        """
        Complete reflex agent cycle:
        Sense -> Perceive -> Calculate -> Decide -> Act
        
        No internal state is maintained between calls
        """
        # Step 1: Perceive
        percepts = self.perceive(sensor_data)
        
        # Step 2: Calculate AQI
        aqi = self.calculate_aqi(percepts)
        aqi_level = self.get_aqi_level(aqi)
        
        # Step 3: Apply rules
        alerts = self.apply_rules(percepts)
        
        # Step 4: Act
        recommendation = self.act(aqi_level)
        
        # Return response
        return {
            'timestamp': datetime.now().isoformat(),
            'aqi_value': aqi,
            'aqi_level': aqi_level,
            'pollutants': percepts,
            'triggered_alerts': alerts,
            'recommendation': recommendation,
            'agent_type': 'Simple Reflex Agent',
            'decision_time_ms': '<1'
        }

# Example usage and testing
if __name__ == "__main__":
    agent = AQIReflexAgent()
    
    # Test Case 1: Good air quality
    print("\n=== Test Case 1: Good Air Quality ===")
    good_data = {
        'pm2_5': 10,
        'pm10': 20,
        'no2': 30,
        'so2': 15,
        'o3': 40
    }
    response = agent.react_to_environment(good_data)
    print(json.dumps(response, indent=2))
    
    # Test Case 2: Poor air quality
    print("\n=== Test Case 2: Poor Air Quality ===")
    poor_data = {
        'pm2_5': 180,
        'pm10': 250,
        'no2': 150,
        'so2': 80,
        'o3': 100
    }
    response = agent.react_to_environment(poor_data)
    print(json.dumps(response, indent=2))
    
    # Test Case 3: Severe air quality
    print("\n=== Test Case 3: Severe Air Quality ===")
    severe_data = {
        'pm2_5': 350,
        'pm10': 400,
        'no2': 250,
        'so2': 150,
        'o3': 200
    }
    response = agent.react_to_environment(severe_data)
    print(json.dumps(response, indent=2))
