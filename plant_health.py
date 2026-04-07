"""
Plant Health Diagnostic Tool
Comprehensive plant disease detection and treatment recommendations
"""

from typing import Dict, List, Tuple

# Comprehensive plant disease database
PLANT_DISEASE_DATABASE = {
    "Powdery Mildew": {
        "symptoms": ["White powder", "Yellow leaves", "White powder on leaves"],
        "severity": "Medium",
        "affected_plants": ["Tomatoes", "Cucumbers", "Squash", "Melons", "Grapes"],
        "treatment": [
            "Remove affected leaves immediately to prevent spread",
            "Apply fungicide containing sulfur or copper",
            "Improve air circulation around plants",
            "Water at soil level to keep leaves dry",
            "Ensure proper spacing between plants",
            "Apply neem oil spray as organic treatment",
            "Monitor humidity levels and reduce if above 70%"
        ]
    },
    
    "Leaf Blight": {
        "symptoms": ["Brown spots", "Yellow leaves", "Brown edges", "Dropping leaves"],
        "severity": "High",
        "affected_plants": ["Tomatoes", "Potatoes", "Peppers", "Eggplant"],
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Apply copper-based fungicide preventatively",
            "Avoid overhead watering to reduce spread",
            "Ensure proper plant spacing for air flow",
            "Rotate crops annually to prevent buildup",
            "Use disease-resistant varieties next season",
            "Sterilize tools between plants to prevent transmission"
        ]
    },
    
    "Root Rot": {
        "symptoms": ["Wilting", "Yellow leaves", "Brown spots near base", "Stunted growth"],
        "severity": "High",
        "affected_plants": ["Tomatoes", "Peppers", "Eggplant", "Cucumbers"],
        "treatment": [
            "Improve soil drainage immediately",
            "Reduce watering frequency",
            "Apply fungicide to soil around affected plants",
            "Remove severely infected plants to prevent spread",
            "Treat soil with beneficial microbes",
            "Avoid overwatering and ensure proper drainage",
            "Consider raised beds for better drainage",
            "Use well-draining soil mixtures"
        ]
    },
    
    "Aphid Infestation": {
        "symptoms": ["Yellow leaves", "Stunted growth", "Holes in leaves", "Sticky residue"],
        "severity": "Medium",
        "affected_plants": ["Tomatoes", "Peppers", "Cucumbers", "Melons", "Leafy greens"],
        "treatment": [
            "Spray with insecticidal soap solution",
            "Release beneficial insects like ladybugs",
            "Apply neem oil or horticultural oil",
            "Remove ants that protect aphids",
            "Use reflective mulch to deter aphids",
            "Prune heavily infested areas",
            "Monitor for natural predators like lacewings"
        ]
    },
    
    "Blossom End Rot": {
        "symptoms": ["Brown spots", "Mold", "Wilting", "Water-soaked lesions"],
        "severity": "High",
        "affected_plants": ["Tomatoes", "Peppers", "Eggplant", "Squash"],
        "treatment": [
            "Apply calcium spray to affected areas",
            "Maintain consistent watering schedule",
            "Ensure proper soil pH (6.5-7.0)",
            "Avoid excessive nitrogen fertilization",
            "Mulch around plants to maintain moisture",
            "Remove affected fruits to prevent spread",
            "Use calcium-rich soil amendments"
        ]
    },
    
    "Early Blight": {
        "symptoms": ["Brown spots", "Wilting", "Brown edges", "Dropping leaves"],
        "severity": "High",
        "affected_plants": ["Tomatoes", "Potatoes", "Peppers"],
        "treatment": [
            "Apply copper-based fungicide at first sign",
            "Remove and destroy infected plant material",
            "Ensure proper spacing for air circulation",
            "Water at base of plants, not on leaves",
            "Use disease-resistant cultivars when possible",
            "Practice crop rotation annually",
            "Sanitize garden tools and equipment"
        ]
    },
    
    "Spider Mites": {
        "symptoms": ["Yellow leaves", "White powder", "Holes in leaves", "Webbing on plants"],
        "severity": "Medium",
        "affected_plants": ["Tomatoes", "Peppers", "Eggplant", "Cucumbers", "Squash"],
        "treatment": [
            "Spray with miticide specifically for spider mites",
            "Increase humidity around plants (mites hate humidity)",
            "Apply predatory mites as biological control",
            "Use neem oil or insecticidal soap",
            "Remove heavily infested leaves",
            "Avoid broad-spectrum pesticides that kill beneficial insects",
            "Monitor undersides of leaves regularly",
            "Maintain plant health to increase resistance"
        ]
    },
    
    "Nutrient Deficiency": {
        "symptoms": ["Yellow leaves", "Stunted growth", "Brown edges", "Dropping leaves"],
        "severity": "Low",
        "affected_plants": ["All plants"],
        "treatment": [
            "Test soil to identify specific nutrient lacking",
            "Apply balanced NPK fertilizer based on test results",
            "For nitrogen deficiency: apply fish emulsion or blood meal",
            "For phosphorus deficiency: apply bone meal or rock phosphate",
            "For potassium deficiency: apply wood ash or potassium sulfate",
            "Adjust soil pH to optimal range (6.0-7.0)",
            "Use organic compost to improve overall soil health",
            "Monitor plant response and adjust fertilization schedule"
        ]
    },
    
    "Bacterial Wilt": {
        "symptoms": ["Wilting", "Yellow leaves", "Brown spots", "Stunted growth"],
        "severity": "High",
        "affected_plants": ["Tomatoes", "Potatoes", "Peppers", "Eggplant"],
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Solarize soil to kill bacteria (cover with clear plastic for 4-6 weeks)",
            "Avoid planting susceptible crops in infected areas for 3-4 years",
            "Use disease-resistant varieties",
            "Practice crop rotation with non-susceptible crops",
            "Ensure proper drainage to prevent bacterial growth",
            "Sterilize tools between plants",
            "Avoid overhead irrigation"
        ]
    },
    
    "Downy Mildew": {
        "symptoms": ["Yellow leaves", "Brown spots", "Mold", "Wilting"],
        "severity": "Medium",
        "affected_plants": ["Grapes", "Cucumbers", "Squash", "Melons"],
        "treatment": [
            "Apply fungicide containing copper or mancozeb",
            "Improve air circulation through proper pruning",
            "Water at soil level, avoid wetting leaves",
            "Ensure proper plant spacing",
            "Apply preventative sprays during humid conditions",
            "Remove affected plant parts",
            "Monitor weather and treat before rainy periods"
        ]
    },
    
    "Tomato Hornworm": {
        "symptoms": ["Holes in leaves", "Dropping leaves", "Pest damage", "Stunted growth"],
        "severity": "Medium",
        "affected_plants": ["Tomatoes", "Peppers", "Eggplant", "Potatoes"],
        "treatment": [
            "Hand-pick larger caterpillars and drop in soapy water",
            "Apply Bt (Bacillus thuringiensis) spray",
            "Release parasitic wasps as biological control",
            "Use row covers to prevent moth egg-laying",
            "Remove weeds that serve as alternate hosts",
            "Monitor plants regularly for early detection",
            "Apply neem oil as organic deterrent"
        ]
    }
}

def diagnose_plant(symptoms: List[str]) -> Dict:
    """Diagnose plant based on symptoms and return condition details"""
    if not symptoms:
        return None
    
    # Clean and normalize symptoms
    cleaned_symptoms = [symptom.strip().lower() for symptom in symptoms if symptom.strip()]
    
    # Symptom mapping for better matching
    symptom_mapping = {
        "white powder": ["white powder", "powdery mildew", "white substance"],
        "yellow leaves": ["yellow", "yellowing", "yellow leaves"],
        "brown spots": ["brown spots", "brown patches", "dark spots"],
        "wilting": ["wilting", "wilt", "drooping", "limp"],
        "stunted growth": ["stunted", "slow growth", "small", "dwarfed"],
        "holes in leaves": ["holes", "chewed leaves", "leaf damage"],
        "dropping leaves": ["dropping", "falling", "losing leaves"],
        "brown edges": ["brown edges", "leaf edges brown", "burnt edges"],
        "mold": ["mold", "mildew", "fungal growth", "fuzzy growth"],
        "pest damage": ["pests", "insects", "bugs", "chewing damage"],
        "webbing": ["webs", "webbing", "spider webs"]
    }
    
    # Normalize symptoms using mapping
    normalized_symptoms = []
    for symptom in cleaned_symptoms:
        found = False
        for key, variations in symptom_mapping.items():
            if symptom in variations:
                normalized_symptoms.append(key)
                found = True
                break
        if not found:
            normalized_symptoms.append(symptom)
    
    # Calculate match scores for each disease
    disease_matches = []
    
    for disease_name, disease_data in PLANT_DISEASE_DATABASE.items():
        disease_symptoms = set([s.lower() for s in disease_data["symptoms"]])
        input_symptoms = set(normalized_symptoms)
        
        # Calculate match percentage
        matches = len(input_symptoms.intersection(disease_symptoms))
        total_symptoms = max(len(input_symptoms), len(disease_symptoms))
        match_percentage = (matches / total_symptoms) * 100 if total_symptoms > 0 else 0
        
        if match_percentage > 0:
            disease_matches.append({
                "disease": disease_name,
                "confidence": round(match_percentage, 1),
                "severity": disease_data["severity"],
                "affected_plants": disease_data["affected_plants"],
                "treatment": disease_data["treatment"]
            })
    
    # Sort by confidence (highest first)
    disease_matches.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Return top match or None if no matches
    if disease_matches:
        return disease_matches[0]
    else:
        return None

def get_all_diseases() -> List[Dict]:
    """Get list of all plant diseases for reference"""
    return [
        {
            "name": disease_name,
            "symptoms": disease_data["symptoms"],
            "severity": disease_data["severity"],
            "affected_plants": disease_data["affected_plants"]
        }
        for disease_name, disease_data in PLANT_DISEASE_DATABASE.items()
    ]

def get_treatment_recommendations(disease_name: str) -> List[str]:
    """Get treatment recommendations for a specific disease"""
    if disease_name in PLANT_DISEASE_DATABASE:
        return PLANT_DISEASE_DATABASE[disease_name]["treatment"]
    else:
        return ["No specific treatment available. Consult local agricultural extension."]

def get_prevention_tips(severity: str) -> List[str]:
    """Get general prevention tips based on severity level"""
    if severity == "High":
        return [
            "Remove and destroy infected plant material immediately",
            "Apply appropriate fungicide or pesticide as soon as symptoms appear",
            "Practice crop rotation to break disease cycles",
            "Ensure proper drainage and air circulation",
            "Use disease-resistant plant varieties when available",
            "Maintain proper soil pH and nutrient levels"
        ]
    elif severity == "Medium":
        return [
            "Monitor plants regularly for early detection",
            "Improve air circulation around plants",
            "Water at soil level to keep foliage dry",
            "Maintain proper plant spacing",
            "Use organic treatments like neem oil when possible",
            "Encourage beneficial insects and organisms"
        ]
    else:  # Low severity
        return [
            "Maintain consistent watering schedule",
            "Ensure proper soil nutrition with balanced fertilization",
            "Monitor plant health regularly",
            "Practice good garden sanitation",
            "Remove dead or dying plant material promptly",
            "Use compost and organic matter to improve soil health"
        ]

def format_plant_diagnosis(diagnosis: Dict) -> str:
    """Format diagnosis result for display"""
    if not diagnosis:
        return "No specific plant condition identified. Monitor plants closely and maintain good growing practices."
    
    formatted = f"""
DIAGNOSIS: {diagnosis['disease']}
Confidence: {diagnosis['confidence']}%
Severity: {diagnosis['severity']}
Affected Plants: {', '.join(diagnosis['affected_plants'])}

RECOMMENDED ACTIONS:
"""
    
    for i, treatment in enumerate(diagnosis['treatment'], 1):
        formatted += f"{i}. {treatment}\n"
    
    return formatted

def main():
    """Main function for plant health testing"""
    print("🌿 Plant Health Diagnostic Tool")
    print("=" * 50)
    print("\nAvailable symptoms for diagnosis:")
    all_symptoms = set()
    for disease_data in PLANT_DISEASE_DATABASE.values():
        all_symptoms.update(disease_data["symptoms"])
    
    for i, symptom in enumerate(sorted(all_symptoms), 1):
        print(f"{i:2d}. {symptom}")
    
    print("\n" + "=" * 50)
    
    while True:
        try:
            print("\nEnter symptoms separated by commas (e.g., yellow leaves, brown spots)")
            print("Type 'quit' to exit")
            
            user_input = input("Symptoms: ").strip()
            
            if user_input.lower() == 'quit':
                print("🌿 Goodbye!")
                break
            
            if user_input:
                symptoms = [s.strip() for s in user_input.split(',') if s.strip()]
                diagnosis = diagnose_plant(symptoms)
                
                if diagnosis:
                    print(f"\n🔍 DIAGNOSIS RESULTS:")
                    print(f"Condition: {diagnosis['disease']}")
                    print(f"Confidence: {diagnosis['confidence']}%")
                    print(f"Severity: {diagnosis['severity']}")
                    
                    print(f"\n🌿 TREATMENT RECOMMENDATIONS:")
                    for i, treatment in enumerate(diagnosis['treatment'], 1):
                        print(f"{i}. {treatment}")
                    
                    print(f"\n⚠️ SEVERITY: {diagnosis['severity']}")
                    prevention_tips = get_prevention_tips(diagnosis['severity'])
                    print("\n🛡️ PREVENTION TIPS:")
                    for tip in prevention_tips:
                        print(f"• {tip}")
                else:
                    print("\n❌ No specific condition identified.")
                    print("Please monitor plants closely and consider consulting agricultural extension.")
            
        except KeyboardInterrupt:
            print("\n🌿 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
