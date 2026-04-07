"""
Crop Inventory Management System
Local database for tracking crop growth and harvest schedules
"""

import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from typing import Dict, List, Tuple
import math

console = Console()

# Data file path
CROPS_FILE = "crops.json"

def load_crops() -> List[Dict]:
    """Load crops from JSON file or return default data"""
    if os.path.exists(CROPS_FILE):
        try:
            with open(CROPS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            console.print("[yellow]Warning: Could not load crops file. Starting with empty inventory.[/yellow]")
    
    # Return empty list by default (no sample data)
    return []

def save_crops(crops: List[Dict]) -> None:
    """Save crops to JSON file"""
    try:
        with open(CROPS_FILE, 'w') as f:
            json.dump(crops, f, indent=2)
    except IOError:
        console.print("[red]Error: Could not save crops to file.[/red]")

def calculate_growth_metrics(planting_date: str, total_days: int) -> Dict:
    """Calculate growth metrics for a crop"""
    try:
        # Parse planting date
        planting_dt = datetime.strptime(planting_date, "%Y-%m-%d")
        current_dt = datetime.now()
        
        # Calculate days passed
        days_passed = (current_dt - planting_dt).days
        
        # Handle negative days (future planting dates)
        if days_passed < 0:
            days_passed = 0
        
        # Calculate growth percentage
        growth_percentage = min((days_passed / total_days) * 100, 100)
        
        # Determine current stage
        if growth_percentage <= 25:
            stage = "Seedling"
            stage_symbol = "S"
        elif growth_percentage <= 50:
            stage = "Vegetative"
            stage_symbol = "V"
        elif growth_percentage <= 75:
            stage = "Flowering"
            stage_symbol = "F"
        else:
            stage = "Harvest Ready"
            stage_symbol = "H"
        
        # Calculate remaining days
        remaining_days = max(total_days - days_passed, 0)
        
        # Calculate days since planting
        days_since_planting = days_passed
        
        return {
            "days_passed": days_passed,
            "growth_percentage": round(growth_percentage, 1),
            "current_stage": stage,
            "stage_symbol": stage_symbol,
            "remaining_days": remaining_days,
            "days_since_planting": days_since_planting,
            "is_overdue": days_passed > total_days,
            "is_future": datetime.strptime(planting_date, "%Y-%m-%d") > current_dt
        }
        
    except ValueError:
        return {
            "days_passed": 0,
            "growth_percentage": 0,
            "current_stage": "Unknown",
            "stage_symbol": "?",
            "remaining_days": total_days,
            "days_since_planting": 0,
            "is_overdue": False,
            "is_future": False
        }

def create_progress_bar(percentage: float, width: 20) -> str:
    """Create a text-based progress bar"""
    filled = int((percentage / 100) * width)
    bar = "=" * filled + "-" * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def display_dashboard(crops: List[Dict]) -> None:
    """Display the crop inventory dashboard"""
    console.print("\n")
    console.print(Panel(
        Text("CROP INVENTORY DASHBOARD", style="bold green"),
        title="Farming Management System",
        border_style="green"
    ))
    
    if not crops:
        console.print(Panel(
            Text("No crops in inventory. Add your first crop to get started!", style="yellow"),
            title="EMPTY INVENTORY",
            border_style="yellow"
        ))
        return
    
    # Create main dashboard table
    dashboard_table = Table(title="Active Crop Inventory", show_header=True, header_style="bold blue")
    dashboard_table.add_column("Crop", style="cyan", width=12)
    dashboard_table.add_column("Field ID", style="white", width=10)
    dashboard_table.add_column("Planting Date", style="yellow", width=12)
    dashboard_table.add_column("Stage", style="green", width=12)
    dashboard_table.add_column("Progress", style="white", width=25)
    dashboard_table.add_column("Days Left", style="magenta", width=10)
    dashboard_table.add_column("Status", style="red", width=10)
    
    for crop in crops:
        metrics = calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])
        
        # Determine status and styling
        if metrics["is_future"]:
            status = "Future"
            status_style = "dim"
        elif metrics["is_overdue"]:
            status = "Overdue"
            status_style = "bold red"
        elif metrics["remaining_days"] <= 7:
            status = "Harvest Soon"
            status_style = "bold yellow"
        else:
            status = "Growing"
            status_style = "green"
        
        # Create progress bar
        progress_bar = create_progress_bar(metrics["growth_percentage"], 15)
        
        # Add row to table
        dashboard_table.add_row(
            crop["crop_name"],
            crop["field_id"],
            crop["planting_date"],
            f"{metrics['stage_symbol']} {metrics['current_stage']}",
            progress_bar,
            str(metrics["remaining_days"]),
            Text(status, style=status_style)
        )
    
    console.print(dashboard_table)
    
    # Summary statistics
    total_crops = len(crops)
    harvest_ready = sum(1 for crop in crops 
                       if calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])["growth_percentage"] >= 75)
    overdue = sum(1 for crop in crops 
                  if calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])["is_overdue"])
    
    summary_text = Text()
    summary_text.append(f"Total Crops: {total_crops}\n", style="bold cyan")
    summary_text.append(f"Harvest Ready: {harvest_ready}\n", style="bold yellow")
    summary_text.append(f"Overdue: {overdue}", style="bold red")
    
    console.print(Panel(
        summary_text,
        title="SUMMARY",
        border_style="blue"
    ))

def add_new_crop() -> None:
    """Add a new crop to the inventory"""
    console.print("\n")
    console.print(Panel(
        Text("ADD NEW CROP", style="bold green"),
        title="Crop Management",
        border_style="green"
    ))
    
    try:
        # Get crop details
        crop_name = Prompt.ask("Enter crop name", default="").strip()
        if not crop_name:
            console.print("[red]Crop name is required.[/red]")
            return
        
        field_id = Prompt.ask("Enter field ID", default="").strip()
        if not field_id:
            console.print("[red]Field ID is required.[/red]")
            return
        
        planting_date = Prompt.ask("Enter planting date (YYYY-MM-DD)", default="").strip()
        if not planting_date:
            console.print("[red]Planting date is required.[/red]")
            return
        
        # Validate date format
        try:
            datetime.strptime(planting_date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/red]")
            return
        
        total_days = IntPrompt.ask("Enter total days to harvest", default=90)
        if total_days <= 0:
            console.print("[red]Days to harvest must be a positive number.[/red]")
            return
        
        # Create new crop entry
        new_crop = {
            "crop_name": crop_name,
            "field_id": field_id,
            "planting_date": planting_date,
            "total_days_to_harvest": total_days
        }
        
        # Load existing crops, add new one, and save
        crops = load_crops()
        crops.append(new_crop)
        save_crops(crops)
        
        console.print(f"[green]Successfully added {crop_name} to inventory![/green]")
        
        # Show the newly added crop details
        metrics = calculate_growth_metrics(planting_date, total_days)
        crop_details = Text()
        crop_details.append(f"Crop: {crop_name}\n", style="bold cyan")
        crop_details.append(f"Field: {field_id}\n", style="white")
        crop_details.append(f"Planted: {planting_date}\n", style="yellow")
        crop_details.append(f"Harvest in: {total_days} days\n", style="magenta")
        crop_details.append(f"Current Stage: {metrics['current_stage']}\n", style="green")
        
        console.print(Panel(
            crop_details,
            title="NEW CROP ADDED",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error adding crop: {e}[/red]")

def delete_crop() -> None:
    """Delete a crop from inventory"""
    console.print("\n")
    console.print(Panel(
        Text("DELETE CROP", style="bold red"),
        title="Crop Management",
        border_style="red"
    ))
    
    crops = load_crops()
    
    if not crops:
        console.print("[yellow]No crops available to delete.[/yellow]")
        return
    
    # Display available crops
    crop_table = Table(title="Available Crops", show_header=True, header_style="bold blue")
    crop_table.add_column("No.", style="cyan", width=5)
    crop_table.add_column("Crop Name", style="white", width=15)
    crop_table.add_column("Field ID", style="yellow", width=10)
    crop_table.add_column("Planting Date", style="green", width=12)
    crop_table.add_column("Days to Harvest", style="magenta", width=15)
    
    for i, crop in enumerate(crops, 1):
        crop_table.add_row(
            str(i),
            crop["crop_name"],
            crop["field_id"],
            crop["planting_date"],
            str(crop["total_days_to_harvest"])
        )
    
    console.print(crop_table)
    
    try:
        # Get user choice
        choice = Prompt.ask("\nEnter crop number to delete (or 'cancel' to abort)", default="cancel").strip()
        
        if choice.lower() == 'cancel':
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        
        try:
            crop_index = int(choice) - 1
            if crop_index < 0 or crop_index >= len(crops):
                console.print("[red]Invalid crop number.[/red]")
                return
            
            # Get crop details for confirmation
            crop_to_delete = crops[crop_index]
            
            # Confirm deletion
            confirm = Prompt.ask(
                f"Are you sure you want to delete '{crop_to_delete['crop_name']}' from field '{crop_to_delete['field_id']}'? (y/n)",
                default="n"
            ).strip().lower()
            
            if confirm == 'y':
                # Remove crop
                deleted_crop = crops.pop(crop_index)
                save_crops(crops)
                console.print(f"[green]Successfully deleted {deleted_crop['crop_name']} from inventory![/green]")
            else:
                console.print("[yellow]Deletion cancelled.[/yellow]")
                
        except ValueError:
            console.print("[red]Invalid input. Please enter a valid crop number.[/red]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error deleting crop: {e}[/red]")

def show_menu() -> None:
    """Display main menu"""
    menu_text = Text()
    menu_text.append("1. View Dashboard\n", style="cyan")
    menu_text.append("2. Add New Crop\n", style="green")
    menu_text.append("3. Delete Crop\n", style="red")
    menu_text.append("4. Exit\n", style="yellow")
    
    console.print(Panel(
        menu_text,
        title="MAIN MENU",
        border_style="blue"
    ))

def get_crops_data() -> List[Dict]:
    """Get crops data with calculated metrics for external use"""
    crops = load_crops()
    crops_with_metrics = []
    
    for crop in crops:
        metrics = calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])
        crop_with_metrics = crop.copy()
        crop_with_metrics.update(metrics)
        crops_with_metrics.append(crop_with_metrics)
    
    return crops_with_metrics

def main():
    """Main function for crop inventory management"""
    console.print("Farming Management System - Crop Inventory", style="bold green")
    console.print("=" * 60)
    
    while True:
        try:
            show_menu()
            choice = Prompt.ask("\nEnter your choice (1-4)", default="1").strip()
            
            if choice == "1":
                crops = load_crops()
                display_dashboard(crops)
                
            elif choice == "2":
                add_new_crop()
                
            elif choice == "3":
                delete_crop()
                
            elif choice == "4":
                console.print("\n[green]Thank you for using Crop Inventory Management![/green]")
                break
                
            else:
                console.print("[red]Invalid choice. Please enter 1, 2, 3, or 4.[/red]")
            
            # Pause before showing menu again
            if choice in ["1", "2", "3"]:
                try:
                    input("\nPress Enter to continue...")
                except EOFError:
                    pass
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {e}[/red]")
            try:
                input("\nPress Enter to continue...")
            except EOFError:
                pass

if __name__ == '__main__':
    main()
