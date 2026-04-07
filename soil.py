#!/usr/bin/env python3
"""
Soil Module for Farming Management System
Provides soil analysis and fertility recommendations based on location
"""

import math
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from typing import Dict, Optional
import sys

console = Console()

def get_soil_profile(lat: float, lon: float) -> Dict[str, float]:
    """
    Smart Mock Data Engine for soil analysis
    Generates realistic soil data based on coordinates
    """
    # Use coordinates to generate consistent but varied data
    # This ensures same coordinates always return same results
    
    # Base values influenced by latitude (climate zones)
    lat_factor = abs(lat) / 90.0  # 0 to 1, from equator to poles
    lon_factor = abs(lon) / 180.0  # 0 to 1, around the globe
    
    # Generate pH based on location (typically 5.5-8.0)
    ph_base = 6.5 + math.sin(lat * 0.1) * 1.0 + math.cos(lon * 0.1) * 0.5
    ph = max(5.5, min(8.0, ph_base))
    
    # Generate Nitrogen (N) in ppm (typically 20-80)
    n_base = 40 + math.sin(lon * 0.15) * 20 + math.cos(lat * 0.12) * 15
    nitrogen = max(20, min(80, n_base))
    
    # Generate Phosphorus (P) in ppm (typically 10-60)
    p_base = 30 + math.cos(lon * 0.13) * 15 + math.sin(lat * 0.11) * 12
    phosphorus = max(10, min(60, p_base))
    
    # Generate Potassium (K) in ppm (typically 100-300)
    k_base = 200 + math.sin(lat * 0.08) * 50 + math.cos(lon * 0.09) * 40
    potassium = max(100, min(300, k_base))
    
    # Generate Moisture % (typically 15-45%)
    moisture_base = 25 + math.sin(lon * 0.14) * 10 + math.cos(lat * 0.16) * 8
    moisture = max(15, min(45, moisture_base))
    
    return {
        'ph': round(ph, 1),
        'nitrogen_ppm': round(nitrogen, 1),
        'phosphorus_ppm': round(phosphorus, 1),
        'potassium_ppm': round(potassium, 1),
        'moisture_percent': round(moisture, 1)
    }

def calculate_fertility(soil_data: Dict[str, float]) -> Dict[str, any]:
    """
    Calculate fertility score and recommend best crops based on N-P-K values
    Returns score (0-100) and crop recommendations
    """
    n = soil_data['nitrogen_ppm']
    p = soil_data['phosphorus_ppm']
    k = soil_data['potassium_ppm']
    ph = soil_data['ph']
    moisture = soil_data['moisture_percent']
    
    # Calculate individual component scores (0-25 each)
    # Nitrogen scoring
    if n >= 60:
        n_score = 25
    elif n >= 40:
        n_score = 20
    elif n >= 30:
        n_score = 15
    elif n >= 20:
        n_score = 10
    else:
        n_score = 5
    
    # Phosphorus scoring
    if p >= 40:
        p_score = 25
    elif p >= 30:
        p_score = 20
    elif p >= 20:
        p_score = 15
    elif p >= 15:
        p_score = 10
    else:
        p_score = 5
    
    # Potassium scoring
    if k >= 200:
        k_score = 25
    elif k >= 150:
        k_score = 20
    elif k >= 120:
        k_score = 15
    elif k >= 100:
        k_score = 10
    else:
        k_score = 5
    
    # pH scoring (optimal range 6.0-7.0)
    if 6.0 <= ph <= 7.0:
        ph_score = 25
    elif 5.5 <= ph <= 7.5:
        ph_score = 20
    elif 5.0 <= ph <= 8.0:
        ph_score = 15
    else:
        ph_score = 10
    
    # Total fertility score
    fertility_score = n_score + p_score + k_score + ph_score
    
    # Determine soil type
    if n > 50 and p > 30 and k > 180:
        soil_type = "Rich Fertile"
    elif n > 35 and p > 20 and k > 140:
        soil_type = "Moderately Fertile"
    elif n > 25 and p > 15 and k > 120:
        soil_type = "Average Fertility"
    else:
        soil_type = "Poor Fertility"
    
    # Crop recommendations based on N-P-K profile
    best_crops = []
    
    # High nitrogen, balanced P-K - good for leafy vegetables
    if n > 45 and p > 25 and k > 150:
        best_crops.extend(["Lettuce", "Spinach", "Cabbage", "Kale"])
    
    # Balanced N-P-K - good for root vegetables
    if 30 <= n <= 50 and 20 <= p <= 35 and 120 <= k <= 200:
        best_crops.extend(["Carrots", "Radishes", "Beets", "Turnips"])
    
    # High phosphorus - good for fruiting plants
    if p > 35 and n > 30:
        best_crops.extend(["Tomatoes", "Peppers", "Eggplant", "Squash"])
    
    # High potassium - good for tubers and grains
    if k > 180 and n > 35:
        best_crops.extend(["Potatoes", "Sweet Potatoes", "Corn", "Wheat"])
    
    # Moisture considerations
    if moisture > 35:
        best_crops.extend(["Rice", "Celery", "Watercress"])
    elif moisture < 20:
        best_crops.extend(["Sorghum", "Millet", "Sunflowers"])
    
    # Remove duplicates and limit to top 6
    best_crops = list(dict.fromkeys(best_crops))[:6]
    
    # Fertility rating
    if fertility_score >= 80:
        rating = "Excellent"
        rating_color = "bright_green"
    elif fertility_score >= 60:
        rating = "Good"
        rating_color = "green"
    elif fertility_score >= 40:
        rating = "Fair"
        rating_color = "yellow"
    else:
        rating = "Poor"
        rating_color = "red"
    
    return {
        'fertility_score': fertility_score,
        'fertility_rating': rating,
        'rating_color': rating_color,
        'soil_type': soil_type,
        'best_crops': best_crops if best_crops else ["General vegetables", "Legumes"],
        'component_scores': {
            'nitrogen': n_score,
            'phosphorus': p_score,
            'potassium': k_score,
            'ph': ph_score
        }
    }

def format_soil_report(lat: float, lon: float, soil_data: Dict, fertility: Dict) -> None:
    """Display formatted soil fertility analysis using rich library"""
    console.print("\n")
    console.print(Panel(
        Text("SOIL FERTILITY ANALYSIS", style="bold green"),
        title="Farming Management System",
        border_style="green"
    ))
    
    # Location info
    location_text = Text()
    location_text.append("Location: ", style="bold")
    location_text.append(f"Coordinates: {lat:.4f}, {lon:.4f}", style="cyan")
    
    console.print(Panel(location_text, title="Analysis Location", border_style="blue"))
    
    # Soil composition table
    soil_table = Table(title="Soil Composition", show_header=True, header_style="bold blue")
    soil_table.add_column("Parameter", style="cyan", width=15)
    soil_table.add_column("Value", style="yellow", width=12)
    soil_table.add_column("Status", style="green", width=10)
    
    # Add soil parameters with status indicators
    ph_status = "Optimal" if 6.0 <= soil_data['ph'] <= 7.0 else "Suboptimal"
    n_status = "High" if soil_data['nitrogen_ppm'] > 50 else "Medium" if soil_data['nitrogen_ppm'] > 30 else "Low"
    p_status = "High" if soil_data['phosphorus_ppm'] > 35 else "Medium" if soil_data['phosphorus_ppm'] > 25 else "Low"
    k_status = "High" if soil_data['potassium_ppm'] > 180 else "Medium" if soil_data['potassium_ppm'] > 140 else "Low"
    moisture_status = "Good" if 20 <= soil_data['moisture_percent'] <= 35 else "Poor"
    
    soil_table.add_row("pH", f"{soil_data['ph']}", ph_status)
    soil_table.add_row("Nitrogen (N)", f"{soil_data['nitrogen_ppm']} ppm", n_status)
    soil_table.add_row("Phosphorus (P)", f"{soil_data['phosphorus_ppm']} ppm", p_status)
    soil_table.add_row("Potassium (K)", f"{soil_data['potassium_ppm']} ppm", k_status)
    soil_table.add_row("Moisture", f"{soil_data['moisture_percent']}%", moisture_status)
    
    console.print(soil_table)

    # Fertility score panel
    score_text = Text()
    score_text.append(f"Fertility Score: ", style="bold")
    score_text.append(f"{fertility['fertility_score']}/100", style=f"bold {fertility['rating_color']}")
    score_text.append(f"Rating: ", style="bold")
    score_text.append(f"{fertility['fertility_rating']}", style=f"bold {fertility['rating_color']}")
    score_text.append(f"Soil Type: ", style="bold")
    score_text.append(f"{fertility['soil_type']}", style="cyan")

    console.print(Panel(score_text, title="Fertility Assessment", border_style=fertility['rating_color']))

    # Component scores
    comp_table = Table(title="Component Breakdown", show_header=True, header_style="bold blue")
    comp_table.add_column("Component", style="cyan", width=12)
    comp_table.add_column("Score", style="yellow", width=8)
    comp_table.add_column("Max", style="dim", width=5)
    
    comp_table.add_row("Nitrogen", str(fertility['component_scores']['nitrogen']), "25")
    comp_table.add_row("Phosphorus", str(fertility['component_scores']['phosphorus']), "25")
    comp_table.add_row("Potassium", str(fertility['component_scores']['potassium']), "25")
    comp_table.add_row("pH Level", str(fertility['component_scores']['ph']), "25")
    
    console.print(comp_table)
    
    # Crop recommendations
    crops_text = Text()
    crops_text.append("Recommended Crops:\n", style="bold green")
    for i, crop in enumerate(fertility['best_crops'], 1):
        crops_text.append(f"  {i}. {crop}\n", style="yellow")
    
    console.print(Panel(crops_text, title="Crop Recommendations", border_style="green"))
    
    console.print("\n")

def main():
    """Main function to run soil analysis"""
    console.print("Farming Management System - Soil Analysis", style="bold green")
    console.print("Enter coordinates for soil analysis (or press Enter for default location)...\n")
    
    try:
        lat_input = input("Enter latitude (-90 to 90) [default: 40.7128]: ").strip()
        lon_input = input("Enter longitude (-180 to 180) [default: -74.0060]: ").strip()
        
        lat = float(lat_input) if lat_input else 40.7128  # New York
        lon = float(lon_input) if lon_input else -74.0060
        
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            console.print("[red]Invalid coordinates. Using default location.[/red]")
            lat, lon = 40.7128, -74.0060
            
    except (ValueError, EOFError):
        console.print("[red]Invalid input or no input detected. Using default coordinates.[/red]")
        lat, lon = 40.7128, -74.0060
    
    console.print(f"\nAnalyzing soil for coordinates: {lat:.4f}, {lon:.4f}\n")
    
    # Get soil profile
    soil_data = get_soil_profile(lat, lon)
    
    # Calculate fertility
    fertility = calculate_fertility(soil_data)
    
    # Display report
    format_soil_report(lat, lon, soil_data, fertility)
    
    return {
        'coordinates': {'latitude': lat, 'longitude': lon},
        'soil_data': soil_data,
        'fertility_analysis': fertility
    }

if __name__ == "__main__":
    main()
