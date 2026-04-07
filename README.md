# Farming Management System

A comprehensive farming management solution with terminal-based tools and a professional web dashboard.

## Components

### Backend Modules
- **weather.py**: Weather risk analysis and alerting
- **soil.py**: Soil fertility analysis and crop recommendations  
- **animal_health.py**: Animal health diagnostic tool
- **crop_inventory.py**: Crop inventory and growth tracking

### Web Application
- **app.py**: Professional Streamlit web dashboard
- **run_app.py**: Easy launcher script

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Verify all modules work:
```bash
python weather.py
python soil.py
python animal_health.py
python crop_inventory.py
```

## Running the Web Application

### Method 1: Using the launcher script
```bash
python run_app.py
```

### Method 2: Direct Streamlit command
```bash
streamlit run app.py
```

The web application will open automatically in your browser at `http://localhost:8501`

## Web Application Features

### 🌾 Farm Overview
- Real-time crop inventory display
- Growth progress bars with visual indicators
- Crop cards showing field ID, stage, and days to harvest
- Summary statistics dashboard

### 🏥 Health & Diagnosis
- Symptom-based animal health diagnosis
- Emergency alerts for high-risk conditions
- Step-by-step emergency procedures
- General wellness advice

### 🌍 Environmental Alerts
- Weather monitoring with risk alerts
- Soil analysis with N-P-K data
- Crop recommendations based on soil profile
- Real-time weather data integration

### Design Features
- **Pure Black Theme** (#000000) with Emerald Green (#2ECC71) accents
- Modern dark-mode SaaS dashboard aesthetic
- Responsive design with custom CSS styling
- Animated status indicators
- Professional card-based layouts

## Terminal Tools

### Weather Analysis
```bash
python weather.py
```
- Automatic geolocation detection
- 7-day weather forecast analysis
- Storm, drought, and heatwave alerts

### Soil Analysis
```bash
python soil.py
```
- Smart mock soil data engine
- Fertility scoring (0-100)
- Crop recommendations based on N-P-K profile

### Animal Health Diagnosis
```bash
python animal_health.py
```
- Symptom-based disease detection
- Emergency procedure guidance
- Risk assessment with confidence scoring

### Crop Inventory Management
```bash
python crop_inventory.py
```
- Add, view, and delete crops
- Growth stage tracking
- Harvest timeline management

## Data Structure

### Crop Data Format
```python
{
    "crop_name": "Wheat",
    "field_id": "North-01", 
    "planting_date": "2024-03-01",
    "total_days_to_harvest": 120
}
```

### Growth Stages
- **Seedling** (0-25%): Early growth phase
- **Vegetative** (26-50%): Leaf development
- **Flowering** (51-75%): Reproduction phase
- **Harvest Ready** (76-100%): Ready for harvest

## API Integration

### Weather Data
- **Source**: Open-Meteo API (free, no API key required)
- **Data**: 7-day forecast with temperature, precipitation, wind speed
- **Alerts**: Storm (>60 km/h), Drought (<1mm/7 days), Heatwave (>38°C)

### Soil Data
- **Source**: Smart mock data engine based on coordinates
- **Parameters**: pH, Nitrogen, Phosphorus, Potassium, Moisture
- **Analysis**: Fertility scoring and crop recommendations

## Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation and display
- `requests`: HTTP client for weather API
- `geocoder`: IP-based geolocation
- `rich`: Terminal formatting and styling

## File Structure

```
Farming Management/
├── app.py                 # Streamlit web application
├── run_app.py            # App launcher script
├── requirements.txt      # Python dependencies
├── weather.py            # Weather analysis module
├── soil.py               # Soil analysis module
├── animal_health.py      # Animal health diagnosis
├── crop_inventory.py     # Crop inventory management
├── crops.json           # Crop data storage (auto-generated)
└── README.md            # This file
```

## Usage Tips

1. **First Time Setup**: Run `python crop_inventory.py` and add some sample crops to see the dashboard in action
2. **Weather Alerts**: The weather module automatically detects your location
3. **Soil Analysis**: Uses default coordinates but can be customized
4. **Animal Health**: Enter symptoms separated by commas for best results
5. **Web Dashboard**: All backend modules are integrated into the web interface

## Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Weather API Issues**: Check internet connection for weather data
3. **Location Detection**: Weather module may need VPN in some regions
4. **Streamlit Not Starting**: Try `pip install --upgrade streamlit`

### Getting Help

- Check the terminal output for specific error messages
- Ensure all Python modules are in the same directory
- Verify internet connectivity for weather features
- Test individual modules before running the web app
