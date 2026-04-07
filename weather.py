#!/usr/bin/env python3
"""
Weather Module for Farming Management System
Provides weather alerts and risk analysis based on current location
"""

import requests
import geocoder
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Dict, List, Optional
import sys

console = Console()

def get_current_location() -> Optional[Dict[str, float]]:
    """Get current GPS coordinates using IP geolocation"""
    try:
        g = geocoder.ip('me')
        if g.ok:
            return {
                'latitude': g.lat,
                'longitude': g.lng,
                'city': g.city,
                'country': g.country
            }
        else:
            console.print("[red]Failed to get location data[/red]")
            return None
    except Exception as e:
        console.print(f"[red]Error getting location: {e}[/red]")
        return None

def get_weather_data(lat: float, lon: float) -> Optional[Dict]:
    """Fetch weather data from Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,precipitation_sum,windspeed_10m_max',
            'forecast_days': 7,
            'timezone': 'auto'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        console.print(f"[red]Error fetching weather data: {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return None

def get_weather_alerts(weather_data: Dict) -> Dict[str, List]:
    """Analyze weather data and generate alerts for farming risks"""
    alerts = {
        'tornado_storm': [],
        'drought': [],
        'heatwave': []
    }
    
    if not weather_data or 'daily' not in weather_data:
        return alerts
    
    daily_data = weather_data['daily']
    dates = daily_data.get('time', [])
    max_temps = daily_data.get('temperature_2m_max', [])
    precipitation = daily_data.get('precipitation_sum', [])
    wind_speeds = daily_data.get('windspeed_10m_max', [])
    
    # Check for tornado/storm conditions
    for i, wind_speed in enumerate(wind_speeds):
        if wind_speed > 60:  # km/h threshold
            alerts['tornado_storm'].append({
                'date': dates[i],
                'wind_speed': wind_speed,
                'severity': 'HIGH' if wind_speed > 80 else 'MODERATE'
            })
    
    # Check for drought conditions
    total_precipitation = sum(precipitation)
    if total_precipitation < 1:  # Less than 1mm over 7 days
        alerts['drought'].append({
            'period': f"Next 7 days",
            'total_precipitation': total_precipitation,
            'severity': 'HIGH' if total_precipitation < 0.5 else 'MODERATE'
        })
    
    # Check for heatwave conditions
    for i, temp in enumerate(max_temps):
        if temp > 38:  # Celsius threshold
            alerts['heatwave'].append({
                'date': dates[i],
                'temperature': temp,
                'severity': 'HIGH' if temp > 42 else 'MODERATE'
            })
    
    return alerts

def format_weather_report(location: Dict, weather_data: Dict, alerts: Dict) -> None:
    """Display formatted weather risk report using rich library"""
    console.print("\n")
    console.print(Panel(
        Text("WEATHER RISK REPORT", style="bold blue"),
        title="Farming Management System",
        border_style="blue"
    ))
    
    # Location info
    location_text = Text()
    location_text.append("Location: ", style="bold")
    location_text.append(f"Location: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}\n", style="cyan")
    location_text.append(f"Coordinates: {location['latitude']:.4f}, {location['longitude']:.4f}", style="cyan")
    
    console.print(Panel(location_text, title="Current Location", border_style="green"))
    
    # Weather summary
    if weather_data and 'daily' in weather_data:
        daily = weather_data['daily']
        avg_temp = sum(daily.get('temperature_2m_max', [])) / len(daily.get('temperature_2m_max', [1]))
        total_precip = sum(daily.get('precipitation_sum', []))
        max_wind = max(daily.get('windspeed_10m_max', [0]))
        
        weather_summary = Text()
        weather_summary.append(f"Avg Max Temp: {avg_temp:.1f}°C\n", style="yellow")
        weather_summary.append(f"Total Precipitation (7 days): {total_precip:.1f}mm\n", style="blue")
        weather_summary.append(f"Max Wind Speed: {max_wind:.1f} km/h", style="cyan")
        
        console.print(Panel(weather_summary, title="Weather Summary", border_style="yellow"))
    
    # Alerts section
    alert_text = Text()
    has_alerts = False
    
    if alerts['tornado_storm']:
        has_alerts = True
        alert_text.append("STORM/TORNADO WARNING:\n", style="bold red")
        for alert in alerts['tornado_storm']:
            alert_text.append(f"  • {alert['date']}: {alert['wind_speed']} km/h ({alert['severity']})\n", style="red")
    
    if alerts['drought']:
        has_alerts = True
        alert_text.append("DROUGHT WARNING:\n", style="bold orange3")
        for alert in alerts['drought']:
            alert_text.append(f"  • {alert['period']}: {alert['total_precipitation']:.1f}mm total ({alert['severity']})\n", style="orange3")
    
    if alerts['heatwave']:
        has_alerts = True
        alert_text.append("HEATWAVE WARNING:\n", style="bold red")
        for alert in alerts['heatwave']:
            alert_text.append(f"  • {alert['date']}: {alert['temperature']:.1f}°C ({alert['severity']})\n", style="red")
    
    if not has_alerts:
        alert_text.append("No significant weather risks detected", style="bold green")
    
    border_style = "red" if has_alerts else "green"
    console.print(Panel(alert_text, title="Weather Alerts", border_style=border_style))
    
    console.print("\n")

def main():
    """Main function to run weather analysis"""
    console.print("Farming Management System - Weather Analysis", style="bold blue")
    console.print("Fetching your location and weather data...\n")
    
    # Get current location
    location = get_current_location()
    if not location:
        console.print("[red]Unable to proceed without location data[/red]")
        sys.exit(1)
    
    # Get weather data
    weather_data = get_weather_data(location['latitude'], location['longitude'])
    if not weather_data:
        console.print("[red]Unable to proceed without weather data[/red]")
        sys.exit(1)
    
    # Generate alerts
    alerts = get_weather_alerts(weather_data)
    
    # Display report
    format_weather_report(location, weather_data, alerts)
    
    return {
        'location': location,
        'weather_data': weather_data,
        'alerts': alerts
    }

if __name__ == "__main__":
    main()
