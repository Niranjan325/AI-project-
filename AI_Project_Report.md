# Air Quality Index (AQI) Monitoring System
## Project Report

### Overview
This project implements a comprehensive Air Quality Index monitoring system with autonomous agent capabilities for real-time air quality tracking and health recommendations.

### Project Structure
```
AI-project/
├── aqi_monitor.py              # Core AQI calculation module
├── aqi_agent/
│   ├── agent.py               # Autonomous AQI agent
│   ├── data.txt               # Sample data
│   └── search/
│       ├── __init__.py
│       └── search.py          # Location-based search module
├── AI_Project_Report.md        # This file
└── README.md                   # Project documentation
```

### Modules

#### 1. AQI Monitor (aqi_monitor.py)
- Calculates AQI values using EPA standards
- Supports multiple pollutants (PM2.5, PM10, O3, NO2, SO2)
- Implements breakpoint method with linear interpolation
- Provides health recommendations

#### 2. AQI Agent (aqi_agent/agent.py)
- Autonomous agent for AQI monitoring
- Real-time location-based queries
- Health alert system
- Search history tracking
- Data export functionality

#### 3. Search Module (aqi_agent/search/search.py)
- Geocoding support
- Location-based AQI fetching
- API integration with OpenWeatherMap

### Key Features

✅ Real-time AQI Calculation
✅ Location-based Air Quality Data
✅ Health Recommendations
✅ Alert Management
✅ Historical Data Tracking
✅ API Integration
✅ Data Export (JSON)

### AQI Categories

| Category | Range | Health Status |
|----------|-------|---------------|
| Good | 0-50 | Safe for outdoor activities |
| Satisfactory | 51-100 | Acceptable air quality |
| Moderately Polluted | 101-150 | Sensitive groups should limit activities |
| Poor | 151-200 | Avoid outdoor activities, use masks |
| Very Poor | 201-300 | Stay indoors, use air purifiers |
| Severe | 301-500 | Dangerous levels, avoid outdoors |

### Usage

```python
from aqi_agent.agent import AQIAgent
from aqi_agent.search import AQISearch

# Initialize agent
agent = AQIAgent(api_key='your_openweather_api_key')

# Search for AQI in a location
result = agent.search_location_aqi('New Delhi', 'IN')

# Get health alert
alert = agent.get_health_alert(aqi_value=150)
```

### API Requirements

- OpenWeatherMap API Key (for real-time data)
- Python 3.8+
- requests library
- python-dotenv for API key management

### Installation

```bash
pip install requests python-dotenv
```

### Future Enhancements

- Machine learning predictions for AQI trends
- Mobile app integration
- Database integration for historical data
- Multi-language support
- Advanced visualization dashboards
- Webhook notifications

### Author

Niranjan325

### License

MIT License
