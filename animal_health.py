"""
Animal Health Diagnostic Tool for Farmers
Terminal-based disease detection and emergency response system
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from typing import Dict, List, Tuple
import re

console = Console()

# Comprehensive livestock disease database
DISEASE_DATABASE = {
    "Foot and Mouth Disease": {
        "symptoms": [
            "blisters", "fever", "lameness", "drooling", "excessive salivation",
            "reluctance to move", "mouth sores", "tongue lesions", "foot lesions",
            "reduced milk production", "weight loss", "loss of appetite"
        ],
        "risk_level": "High/SOS",
        "emergency_procedures": [
            "IMMEDIATELY isolate the affected animal",
            "Contact your veterinarian immediately",
            "Report to local agricultural authorities",
            "Quarantine the entire herd/flock",
            "Disinfect all equipment and facilities",
            "Restrict movement of all animals",
            "Wear protective clothing when handling animals",
            "Monitor other animals for symptoms"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "pigs"]
    },
    
    "Anthrax": {
        "symptoms": [
            "sudden death", "high fever", "difficulty breathing", "bloody discharge",
            "swelling", "depression", "loss of appetite", "trembling", "convulsions",
            "dark bloody discharge from nose, mouth, or anus", "rapid pulse", "collapse"
        ],
        "risk_level": "High/SOS",
        "emergency_procedures": [
            "DO NOT handle the carcass - Anthrax spores are dangerous to humans",
            "Contact authorities immediately - this is a reportable disease",
            "Evacuate the area if possible",
            "Quarantine the entire farm",
            "Burn or bury the carcass under supervision",
            "Disinfect the area with appropriate agents",
            "Vaccinate remaining animals if advised",
            "Use full protective equipment if handling is unavoidable"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "horses"]
    },
    
    "Bloat": {
        "symptoms": [
            "distended abdomen", "difficulty breathing", "belching", "restlessness",
            "staggering", "groaning", "lying down frequently", "rapid breathing",
            "enlarged left side", "drooling", "grinding teeth"
        ],
        "risk_level": "High/SOS",
        "emergency_procedures": [
            "Keep the animal walking and standing",
            "Call veterinarian immediately",
            "Do not allow the animal to lie down",
            "Administer approved anti-foaming agents if available",
            "Pass a stomach tube if trained to do so",
            "Avoid feeding until veterinarian arrives",
            "Monitor breathing continuously",
            "Prepare for emergency rumenotomy if needed"
        ],
        "affected_animals": ["cattle", "sheep", "goats"]
    },
    
    "Milk Fever": {
        "symptoms": [
            "muscle weakness", "cold ears", "staggering", "inability to stand",
            "depression", "loss of appetite", "constipation", "dry muzzle",
            "subnormal temperature", "dilated pupils", "coma"
        ],
        "risk_level": "High/SOS",
        "emergency_procedures": [
            "Call veterinarian immediately",
            "Administer calcium solution if prescribed",
            "Keep the animal warm",
            "Provide intravenous calcium if trained",
            "Monitor heart rate and temperature",
            "Keep the animal in sternal recumbency",
            "Provide supportive care",
            "Prevent aspiration pneumonia"
        ],
        "affected_animals": ["cattle", "goats"]
    },
    
    "Mastitis": {
        "symptoms": [
            "swollen udder", "hard udder", "painful udder", "abnormal milk",
            "clots in milk", "watery milk", "bloody milk", "fever", "depression",
            "loss of appetite", "reduced milk production"
        ],
        "risk_level": "Medium",
        "emergency_procedures": [
            "Begin antibiotic therapy as prescribed",
            "Apply hot packs to udder",
            "Milk out frequently (every 2-4 hours)",
            "Increase fluid intake",
            "Isolate the animal if contagious",
            "Maintain proper milking hygiene",
            "Monitor temperature and appetite",
            "Consult veterinarian for proper treatment"
        ],
        "affected_animals": ["cattle", "goats", "sheep"]
    },
    
    "Pneumonia": {
        "symptoms": [
            "coughing", "difficulty breathing", "rapid breathing", "fever",
            "nasal discharge", "loss of appetite", "depression", "weight loss",
            "grunting sounds", "open mouth breathing"
        ],
        "risk_level": "Medium",
        "emergency_procedures": [
            "Move to well-ventilated area",
            "Provide antibiotics as prescribed",
            "Monitor temperature regularly",
            "Ensure adequate hydration",
            "Reduce stress on the animal",
            "Isolate from healthy animals",
            "Consult veterinarian for treatment plan",
            "Monitor for secondary infections"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "pigs"]
    },
    
    "Diarrhea (Scours)": {
        "symptoms": [
            "watery feces", "frequent defecation", "dehydration", "loss of appetite",
            "weight loss", "weakness", "sunken eyes", "poor coat condition",
            "blood in stool", "mucus in stool"
        ],
        "risk_level": "Medium",
        "emergency_procedures": [
            "Provide clean water immediately",
            "Administer electrolytes if available",
            "Isolate from other animals",
            "Clean contaminated areas",
            "Monitor for dehydration signs",
            "Withhold food for 12-24 hours if severe",
            "Consult veterinarian for medication",
            "Maintain proper hygiene"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "pigs"]
    },
    
    "Lameness": {
        "symptoms": [
            "limping", "reluctance to move", "swollen joints", "pain when walking",
            "abnormal gait", "lying down frequently", "reluctance to stand",
            "heat in joints", "reduced weight bearing", "stiff movement"
        ],
        "risk_level": "Low",
        "emergency_procedures": [
            "Examine the affected limb carefully",
            "Provide rest and isolation",
            "Apply cold compresses if swelling",
            "Check for foreign objects in hooves",
            "Consult veterinarian if persistent",
            "Maintain clean, dry bedding",
            "Monitor for improvement",
            "Consider nutritional supplements"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "horses", "pigs"]
    },
    
    "Parasites": {
        "symptoms": [
            "weight loss", "poor coat condition", "diarrhea", "anemia",
            "bottle jaw", "rough hair coat", "reduced production", "lethargy",
            "pot belly", "coughing (lungworms)"
        ],
        "risk_level": "Low",
        "emergency_procedures": [
            "Administer deworming medication",
            "Improve pasture management",
            "Provide clean water and nutrition",
            "Test fecal samples if possible",
            "Implement regular deworming schedule",
            "Separate affected animals",
            "Monitor weight and condition",
            "Consult veterinarian for treatment plan"
        ],
        "affected_animals": ["cattle", "sheep", "goats", "horses", "pigs"]
    }
}

def clean_symptoms(symptom_input: str) -> List[str]:
    """Clean and normalize user input symptoms"""
    if not symptom_input:
        return []
    
    # Convert to lowercase and split by commas
    symptoms = [symptom.strip().lower() for symptom in symptom_input.split(',')]
    
    # Remove empty strings and extra spaces
    symptoms = [symptom.strip() for symptom in symptoms if symptom.strip()]
    
    # Normalize common variations
    symptom_mapping = {
        "limp": "limping",
        "lameness": "limping",
        "sore feet": "limping",
        "hard to walk": "limping",
        "bloated": "bloat",
        "swollen belly": "bloat",
        "big stomach": "bloat",
        "feverish": "fever",
        "hot": "fever",
        "high temp": "fever",
        "temperature": "fever",
        "not eating": "loss of appetite",
        "no appetite": "loss of appetite",
        "refusing food": "loss of appetite",
        "sad": "depression",
        "lethargic": "depression",
        "no energy": "depression",
        "sore udder": "swollen udder",
        "painful udder": "swollen udder",
        "bad milk": "abnormal milk",
        "clotty milk": "clots in milk",
        "watery milk": "abnormal milk",
        "cough": "coughing",
        "breathing hard": "difficulty breathing",
        "fast breathing": "rapid breathing",
        "runny nose": "nasal discharge",
        "sick": "depression",
        "weak": "weakness",
        "tired": "weakness",
        "thin": "weight loss",
        "losing weight": "weight loss"
    }
    
    # Apply symptom mapping
    normalized_symptoms = []
    for symptom in symptoms:
        if symptom in symptom_mapping:
            normalized_symptoms.append(symptom_mapping[symptom])
        else:
            normalized_symptoms.append(symptom)
    
    return normalized_symptoms

def calculate_match_confidence(user_symptoms: List[str], disease_symptoms: List[str]) -> float:
    """Calculate match confidence percentage"""
    if not user_symptoms:
        return 0.0
    
    # Count matching symptoms
    matches = sum(1 for symptom in user_symptoms if symptom in disease_symptoms)
    
    # Calculate confidence based on matches and total symptoms
    confidence = (matches / len(user_symptoms)) * 100
    
    # Boost confidence if multiple key symptoms match
    key_symptoms = ["fever", "sudden death", "blisters", "difficulty breathing", "swollen udder"]
    key_matches = sum(1 for symptom in user_symptoms if symptom in key_symptoms and symptom in disease_symptoms)
    
    if key_matches >= 2:
        confidence = min(confidence + 20, 100)  # Boost by 20% but cap at 100%
    
    return round(confidence, 1)

def diagnose_animal(user_symptoms: List[str]) -> List[Tuple[str, float, Dict]]:
    """Diagnose animal based on symptoms and return matches with confidence"""
    matches = []
    
    for disease_name, disease_data in DISEASE_DATABASE.items():
        confidence = calculate_match_confidence(user_symptoms, disease_data["symptoms"])
        
        if confidence > 0:  # Only include diseases with some match
            matches.append((disease_name, confidence, disease_data))
    
    # Sort by confidence (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches

def display_emergency_alert(disease_name: str, disease_data: Dict, confidence: float):
    """Display emergency alert for high-risk conditions"""
    console.print("\n")
    
    # Create emergency alert panel
    alert_text = Text()
    alert_text.append("EMERGENCY ACTION REQUIRED", style="bold red")
    
    console.print(Panel(
        alert_text,
        title="CRITICAL ALERT",
        border_style="red",
        padding=(1, 2)
    ))
    
    # Disease information
    disease_info = Text()
    disease_info.append(f"Diagnosed Condition: ", style="bold")
    disease_info.append(f"{disease_name}\n", style="bold red")
    disease_info.append(f"Match Confidence: ", style="bold")
    disease_info.append(f"{confidence}%\n", style="bold yellow")
    disease_info.append(f"Risk Level: ", style="bold")
    disease_info.append(f"{disease_data['risk_level']}", style="bold red")
    
    console.print(Panel(
        disease_info,
        title="DIAGNOSIS",
        border_style="yellow"
    ))
    
    # Emergency procedures
    procedures_text = Text()
    procedures_text.append("IMMEDIATE FIRST AID PROCEDURES:\n\n", style="bold red")
    
    for i, procedure in enumerate(disease_data["emergency_procedures"], 1):
        procedures_text.append(f"{i}. {procedure}\n", style="white")
    
    console.print(Panel(
        procedures_text,
        title="FIRST AID - ACT NOW",
        border_style="red"
    ))
    
    console.print("\n")

def display_diagnostic_results(matches: List[Tuple[str, float, Dict]]):
    """Display diagnostic results for non-emergency cases"""
    console.print("\n")
    console.print(Panel(
        Text("ANIMAL HEALTH DIAGNOSTIC RESULTS", style="bold blue"),
        title="Farming Management System",
        border_style="blue"
    ))
    
    if not matches:
        console.print(Panel(
            Text("No specific conditions matched based on the symptoms provided.", style="yellow"),
            title="NO CLEAR DIAGNOSIS",
            border_style="yellow"
        ))
        display_general_advice()
        return
    
    # Create results table
    results_table = Table(title="Potential Conditions", show_header=True, header_style="bold blue")
    results_table.add_column("Condition", style="cyan", width=25)
    results_table.add_column("Confidence", style="yellow", width=12)
    results_table.add_column("Risk Level", style="red", width=12)
    
    high_risk_found = False
    
    for disease_name, confidence, disease_data in matches:
        risk_style = "bold red" if disease_data["risk_level"] == "High/SOS" else "yellow"
        results_table.add_row(
            disease_name,
            f"{confidence}%",
            disease_data["risk_level"],
            style=risk_style
        )
        
        if disease_data["risk_level"] == "High/SOS" and confidence >= 50:
            high_risk_found = True
    
    console.print(results_table)
    
    # If high risk conditions found, show detailed alert
    if high_risk_found:
        for disease_name, confidence, disease_data in matches:
            if disease_data["risk_level"] == "High/SOS" and confidence >= 50:
                display_emergency_alert(disease_name, disease_data, confidence)
                break
    else:
        # Show top match details
        if matches:
            top_match = matches[0]
            disease_name, confidence, disease_data = top_match
            
            details_text = Text()
            details_text.append(f"Most Likely Condition: ", style="bold")
            details_text.append(f"{disease_name}\n", style="bold cyan")
            details_text.append(f"Confidence: {confidence}%\n", style="yellow")
            details_text.append(f"Risk Level: {disease_data['risk_level']}\n\n", style="yellow")
            details_text.append("Common Symptoms:\n", style="bold")
            
            for symptom in disease_data["symptoms"][:5]:  # Show first 5 symptoms
                details_text.append(f"• {symptom}\n", style="white")
            
            console.print(Panel(
                details_text,
                title="TOP MATCH DETAILS",
                border_style="cyan"
            ))
            
            # Show recommended actions
            actions_text = Text()
            actions_text.append("Recommended Actions:\n\n", style="bold green")
            
            for i, procedure in enumerate(disease_data["emergency_procedures"][:3], 1):  # Show first 3 procedures
                actions_text.append(f"{i}. {procedure}\n", style="white")
            
            actions_text.append(f"\n{'...' if len(disease_data['emergency_procedures']) > 3 else ''}", style="dim")
            
            console.print(Panel(
                actions_text,
                title="RECOMMENDED ACTIONS",
                border_style="green"
            ))

def display_general_advice():
    """Display general wellness advice when no clear diagnosis"""
    advice_text = Text()
    advice_text.append("GENERAL WELLNESS ADVICE:\n\n", style="bold green")
    advice_text.append("1. Monitor the animal closely for any changes\n", style="white")
    advice_text.append("2. Ensure access to clean water and quality feed\n", style="white")
    advice_text.append("3. Maintain clean, dry bedding\n", style="white")
    advice_text.append("4. Isolate from other animals if symptoms persist\n", style="white")
    advice_text.append("5. Check temperature and vital signs regularly\n", style="white")
    advice_text.append("6. Review recent changes in diet or environment\n", style="white")
    
    console.print(Panel(
        advice_text,
        title="GENERAL CARE",
        border_style="green"
    ))
    
    # Vet reminder
    vet_text = Text()
    vet_text.append("CALL A VETERINARIAN IF:", style="bold red")
    vet_text.append("\n\n", style="bold red")
    vet_text.append("• Symptoms persist for more than 24 hours\n", style="white")
    vet_text.append("• Animal's condition worsens\n", style="white")
    vet_text.append("• Multiple animals show similar symptoms\n", style="white")
    vet_text.append("• Animal appears to be in pain or distress\n", style="white")
    vet_text.append("• You notice sudden behavioral changes\n", style="white")
    
    console.print(Panel(
        vet_text,
        title="WHEN TO CONTACT A VET",
        border_style="red"
    ))

def main():
    """Main function for animal health diagnostic tool"""
    console.print("Farming Management System - Animal Health Diagnostic Tool", style="bold blue")
    console.print("=" * 70)
    console.print("\n")
    
    console.print("Enter symptoms separated by commas (e.g., 'fever, limping, blisters')", style="cyan")
    console.print("Common symptoms: fever, limping, swelling, diarrhea, coughing, loss of appetite", style="dim")
    console.print("\n")
    
    # Get user input
    symptom_input = Prompt.ask("Enter observed symptoms", default="")
    
    if not symptom_input.strip():
        console.print("[yellow]No symptoms entered. Please observe your animal and try again.[/yellow]")
        return
    
    # Clean and process symptoms
    user_symptoms = clean_symptoms(symptom_input)
    
    if not user_symptoms:
        console.print("[yellow]No valid symptoms detected. Please check your input and try again.[/yellow]")
        return
    
    console.print(f"\nAnalyzing symptoms: {', '.join(user_symptoms)}", style="cyan")
    console.print("Running diagnostic analysis...\n", style="dim")
    
    # Perform diagnosis
    matches = diagnose_animal(user_symptoms)
    
    # Display results
    display_diagnostic_results(matches)
    
    return matches

if __name__ == '__main__':
    main()
