"""
AgriCommand - Complete Farming Management Dashboard
Professional Streamlit integration of all farming modules
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import local modules
try:
    import weather
    import soil
    import animal_health
    import crop_inventory
    # Try to import plant_health (may not exist yet)
    try:
        import plant_health
        PLANT_HEALTH_AVAILABLE = True
    except ImportError:
        PLANT_HEALTH_AVAILABLE = False
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Page Configuration
st.set_page_config(
    layout='wide',
    page_title='AgriCommand',
    initial_sidebar_state='expanded'
)

# Custom CSS Styling
def apply_custom_styling():
    """Apply custom dark theme styling"""
    st.markdown("""
    <style>
    /* Main theme colors */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Hide Streamlit elements */
    .stMainMenu {
        visibility: hidden;
    }
    
    .stHeader {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
        height: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0a0a0a;
        border-right: 2px solid #2ECC71;
    }
    
    /* Button styling */
    div.stButton > button:first-child {
        background-color: #2ECC71;
        color: #000000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(46, 204, 113, 0.2);
    }
    
    div.stButton > button:first-child:hover {
        background-color: #27AE60;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 204, 113, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #2ECC71;
        border-radius: 4px;
    }
    
    /* Card styling */
    .crop-card {
        background-color: #0a0a0a;
        border: 1px solid #2ECC71;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(46, 204, 113, 0.1);
        transition: all 0.3s ease;
    }
    
    .crop-card:hover {
        box-shadow: 0 6px 12px rgba(46, 204, 113, 0.2);
        transform: translateY(-2px);
    }
    
    /* Alert banner styling */
    .alert-banner {
        background-color: #e74c3c;
        color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
        border-left: 4px solid #c0392b;
        box-shadow: 0 2px 4px rgba(231, 76, 60, 0.2);
    }
    
    .warning-banner {
        background-color: #f39c12;
        color: #000000;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
        border-left: 4px solid #e67e22;
        box-shadow: 0 2px 4px rgba(243, 156, 18, 0.2);
    }
    
    /* Status indicator */
    .status-online {
        color: #2ECC71;
        font-weight: bold;
        display: flex;
        align-items: center;
        background-color: #0a0a0a;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border: 1px solid #2ECC71;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #2ECC71;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Table styling */
    .dataframe {
        background-color: #0a0a0a;
        color: #FFFFFF;
        border: 1px solid #2ECC71;
        border-radius: 8px;
    }
    
    .dataframe th {
        background-color: #2ECC71;
        color: #000000;
        font-weight: bold;
        text-align: center;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #0a0a0a;
        color: #FFFFFF;
        border: 1px solid #2ECC71;
        border-radius: 6px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        background-color: #0a0a0a;
        color: #FFFFFF;
        border: 1px solid #2ECC71;
        border-radius: 6px;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background-color: #0a0a0a;
        border: 1px solid #2ECC71;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background-color: #0a0a0a;
        border: 1px solid #2ECC71;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2ECC71;
        color: #000000;
    }
    
    /* Metric card styling */
    .metric-card {
        background-color: #0a0a0a;
        border: 1px solid #2ECC71;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(46, 204, 113, 0.1);
    }
    
    /* Header styling */
    .main-header {
        color: #2ECC71;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sub-header {
        color: #FFFFFF;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
        opacity: 0.8;
    }
    
    /* Form styling */
    .form-container {
        background-color: #0a0a0a;
        border: 1px solid #2ECC71;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create sidebar with navigation and status"""
    with st.sidebar:
        # Farm Logo placeholder
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border-bottom: 2px solid #2ECC71; margin-bottom: 1rem;">
            <div style="font-size: 2rem; color: #2ECC71; font-weight: bold;">🌾</div>
            <div style="color: #FFFFFF; font-size: 0.9rem; margin-top: 0.5rem;">AgriCommand</div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status
        st.markdown("""
        <div class="status-online">
            <div class="status-dot"></div>
            System Status: ONLINE
        </div>
        """, unsafe_allow_html=True)
        
        # Current Date/Time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"""
        <div style="color: #FFFFFF; font-size: 0.9rem; margin: 1rem 0; text-align: center;">
            📅 {current_time}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Menu
        page = st.radio(
            "🧭 Navigation",
            ["📊 Dashboard", "🩺 Health & Diagnosis", "📡 Environmental Alerts"],
            index=0,
            key="navigation"
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        try:
            crops = crop_inventory.load_crops()
            st.metric("🌱 Active Crops", len(crops))
        except:
            st.metric("🌱 Active Crops", "N/A")
        
        # System Info
        st.markdown("### ℹ️ System Info")
        st.markdown("**Version:** 2.0.0")
        st.markdown("**Modules:** 5 Active")
    
    return page

def dashboard_page():
    """Dashboard page with crop inventory management"""
    st.markdown('<h1 class="main-header">📊 Farm Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Complete crop inventory and management system</p>', unsafe_allow_html=True)
    
    # Summary Statistics
    try:
        crops = crop_inventory.load_crops()
        
        if not crops:
            total_crops = 0
            harvest_ready = 0
            overdue = 0
        else:
            total_crops = len(crops)
            harvest_ready = sum(1 for crop in crops 
                               if crop_inventory.calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])["growth_percentage"] >= 75)
            overdue = sum(1 for crop in crops 
                         if crop_inventory.calculate_growth_metrics(crop["planting_date"], crop["total_days_to_harvest"])["is_overdue"])
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌱 Total Crops", total_crops, delta=None)
        with col2:
            st.metric("🌾 Harvest Ready", harvest_ready, delta=None)
        with col3:
            st.metric("⚠️ Overdue", overdue, delta=None)
        
        st.markdown("---")
        
        # Crop Management Section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### ➕ Add New Crop")
            with st.form("add_crop_form"):
                crop_name = st.text_input("Crop Name*", placeholder="e.g., Wheat, Corn")
                field_id = st.text_input("Field ID*", placeholder="e.g., North-01")
                planting_date = st.date_input("Planting Date*", datetime.now())
                total_days = st.number_input("Days to Harvest*", min_value=1, max_value=365, value=90)
                
                submitted = st.form_submit_button("🌱 Add Crop", type="primary")
                
                if submitted:
                    if crop_name and field_id:
                        try:
                            new_crop = {
                                "crop_name": crop_name,
                                "field_id": field_id,
                                "planting_date": planting_date.strftime("%Y-%m-%d"),
                                "total_days_to_harvest": int(total_days)
                            }
                            
                            crops = crop_inventory.load_crops()
                            crops.append(new_crop)
                            crop_inventory.save_crops(crops)
                            
                            st.success(f"✅ Successfully added {crop_name}!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    else:
                        st.error("⚠️ Please fill all required fields")
        
        with col2:
            st.markdown("### 🗑️ Delete Crop")
            if not crops:
                st.info("📭 No crops to delete")
            else:
                with st.form("delete_crop_form"):
                    crop_options = [f"{crop['crop_name']} - {crop['field_id']}" for crop in crops]
                    selected_index = st.selectbox("Select crop", range(len(crop_options)), format_func=lambda x: crop_options[x])
                    
                    delete_submitted = st.form_submit_button("🗑️ Delete Crop", type="secondary")
                    
                    if delete_submitted:
                        try:
                            crop_to_delete = crops[selected_index]
                            crops.pop(selected_index)
                            crop_inventory.save_crops(crops)
                            st.success(f"✅ Deleted {crop_to_delete['crop_name']}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        st.markdown("---")
        
        # Crop Display
        st.markdown("### 🌱 Current Crops")
        
        if not crops:
            st.warning("🌱 No crops in inventory. Add your first crop above!")
        else:
            # Display crops in grid
            cols = st.columns(3)
            
            for i, crop in enumerate(crops):
                with cols[i % 3]:
                    metrics = crop_inventory.calculate_growth_metrics(
                        crop["planting_date"], 
                        crop["total_days_to_harvest"]
                    )
                    
                    # Create crop card
                    st.markdown(f"""
                    <div class="crop-card">
                        <h4 style="color: #2ECC71; margin-bottom: 0.5rem;">🌱 {crop['crop_name']}</h4>
                        <p style="margin: 0.25rem 0;"><strong>Field:</strong> {crop['field_id']}</p>
                        <p style="margin: 0.25rem 0;"><strong>Stage:</strong> {metrics['current_stage']}</p>
                        <p style="margin: 0.25rem 0;"><strong>Days Left:</strong> {metrics['remaining_days']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    st.progress(metrics['growth_percentage'] / 100)
                    
                    # Status
                    if metrics['is_overdue']:
                        st.error("⚠️ Overdue")
                    elif metrics['remaining_days'] <= 7:
                        st.warning("⏰ Harvest Soon")
                    else:
                        st.success("✅ Growing")
                        
    except Exception as e:
        st.error(f"Dashboard Error: {e}")

def health_diagnosis_page():
    """Health & Diagnosis page with livestock and crops tabs"""
    st.markdown('<h1 class="main-header">🩺 Health & Diagnosis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive health analysis for animals and plants</p>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["🐄 Livestock", "🌿 Crops"])
    
    with tab1:
        st.markdown("### 🐄 Livestock Health Diagnosis")
        
        # Symptom selection
        st.markdown("#### 🔍 Enter Symptoms")
        symptoms_input = st.text_input(
            "Enter symptoms separated by commas (e.g., fever, limping, blisters)",
            placeholder="fever, limping, blisters",
            key="livestock_symptoms"
        )
        
        if st.button("🔬 Diagnose Livestock", key="diagnose_livestock"):
            if symptoms_input.strip():
                try:
                    user_symptoms = animal_health.clean_symptoms(symptoms_input)
                    matches = animal_health.diagnose_animal(user_symptoms)
                    
                    if matches:
                        # Check for high-risk conditions
                        high_risk_found = False
                        for disease_name, confidence, disease_data in matches:
                            if disease_data["risk_level"] == "High/SOS" and confidence >= 50:
                                high_risk_found = True
                                break
                        
                        if high_risk_found:
                            # Emergency alert
                            st.markdown("""
                            <div class="alert-banner">
                                ⚠️ EMERGENCY ACTION REQUIRED
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for disease_name, confidence, disease_data in matches:
                                if disease_data["risk_level"] == "High/SOS" and confidence >= 50:
                                    st.error(f"**Diagnosed:** {disease_name}")
                                    st.error(f"**Confidence:** {confidence}%")
                                    st.error(f"**Risk Level:** {disease_data['risk_level']}")
                                    
                                    st.markdown("### 🚑 Emergency Procedures")
                                    for i, procedure in enumerate(disease_data["emergency_procedures"], 1):
                                        st.write(f"{i}. {procedure}")
                                    break
                        else:
                            # Show all matches
                            results_data = []
                            for disease_name, confidence, disease_data in matches:
                                results_data.append({
                                    "Condition": disease_name,
                                    "Confidence": f"{confidence}%",
                                    "Risk Level": disease_data["risk_level"]
                                })
                            
                            df = pd.DataFrame(results_data)
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.info("ℹ️ No specific conditions matched. Monitor animal closely.")
                        
                except Exception as e:
                    st.error(f"Diagnosis Error: {e}")
            else:
                st.warning("⚠️ Please enter symptoms to diagnose")
    
    with tab2:
        st.markdown("### 🌿 Crop Health Diagnosis")
        
        if PLANT_HEALTH_AVAILABLE:
            # Plant symptom selection
            st.markdown("#### 🔍 Enter Plant Symptoms")
            plant_symptoms = st.multiselect(
                "Select plant symptoms:",
                ["Yellow leaves", "Brown spots", "Wilting", "Stunted growth", "White powder", 
                 "Holes in leaves", "Dropping leaves", "Brown edges", "Mold", "Pest damage"],
                key="plant_symptoms"
            )
            
            if st.button("🔬 Diagnose Plants", key="diagnose_plants"):
                if plant_symptoms:
                    try:
                        # Call plant health diagnosis
                        diagnosis = plant_health.diagnose_plant(plant_symptoms)
                        
                        if diagnosis:
                            if diagnosis['severity'] == 'High':
                                st.error(f"**Condition:** {diagnosis['disease']}")
                                st.error(f"**Severity:** {diagnosis['severity']}")
                                st.markdown("### 🌿 Treatment Advice")
                                for advice in diagnosis['treatment']:
                                    st.write(f"• {advice}")
                            else:
                                st.warning(f"**Condition:** {diagnosis['disease']}")
                                st.warning(f"**Severity:** {diagnosis['severity']}")
                                st.markdown("### 🌿 Treatment Advice")
                                for advice in diagnosis['treatment']:
                                    st.write(f"• {advice}")
                        else:
                            st.info("ℹ️ No specific condition identified. Monitor plants closely.")
                            
                    except Exception as e:
                        st.error(f"Plant Diagnosis Error: {e}")
                else:
                    st.warning("⚠️ Please select symptoms to diagnose")
        else:
            st.info("🌿 Plant health module not available. This feature requires plant_health.py module.")

def environmental_alerts_page():
    """Environmental Alerts page with weather and soil data"""
    st.markdown('<h1 class="main-header">📡 Environmental Alerts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time weather monitoring and soil analysis</p>', unsafe_allow_html=True)
    
    # Weather Alerts Section
    st.markdown("### 🌤️ Weather Monitoring")
    
    try:
        location = weather.get_current_location()
        if location:
            weather_data = weather.get_weather_data(location['latitude'], location['longitude'])
            alerts = weather.get_weather_alerts(weather_data)
            
            # Display weather alerts
            if any(alerts.values()):
                if alerts['tornado_storm']:
                    st.markdown(f"""
                    <div class="alert-banner">
                        🌪️ STORM/TORNADO WARNING
                        <br>Wind speeds: {alerts['tornado_storm'][0]['wind_speed']} km/h
                    </div>
                    """, unsafe_allow_html=True)
                
                if alerts['drought']:
                    st.markdown(f"""
                    <div class="warning-banner">
                        🏜️ DROUGHT WARNING
                        <br>Precipitation: {alerts['drought'][0]['total_precipitation']}mm (7 days)
                    </div>
                    """, unsafe_allow_html=True)
                
                if alerts['heatwave']:
                    st.markdown(f"""
                    <div class="alert-banner">
                        🔥 HEATWAVE WARNING
                        <br>Temperature: {alerts['heatwave'][0]['temperature']}°C
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No significant weather risks detected")
            
            # Weather metrics
            if weather_data and 'daily' in weather_data:
                daily = weather_data['daily']
                avg_temp = sum(daily.get('temperature_2m_max', [])) / len(daily.get('temperature_2m_max', [1]))
                total_precip = sum(daily.get('precipitation_sum', []))
                max_wind = max(daily.get('windspeed_10m_max', [0]))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🌡️ Avg Temp", f"{avg_temp:.1f}°C")
                with col2:
                    st.metric("💧 Precipitation", f"{total_precip:.1f}mm")
                with col3:
                    st.metric("💨 Max Wind", f"{max_wind:.1f} km/h")
        else:
            st.error("❌ Unable to get weather data")
            
    except Exception as e:
        st.error(f"Weather Error: {e}")
    
    st.markdown("---")
    
    # Soil Analysis Section
    st.markdown("### 🌱 Soil Analysis")
    
    try:
        # Get soil data
        lat, lon = 40.7128, -74.0060  # Default coordinates
        soil_data = soil.get_soil_profile(lat, lon)
        fertility = soil.calculate_fertility(soil_data)
        
        # Create soil data table
        soil_table_data = {
            "Parameter": ["pH", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Moisture"],
            "Value": [
                f"{soil_data['ph']}",
                f"{soil_data['nitrogen_ppm']} ppm",
                f"{soil_data['phosphorus_ppm']} ppm", 
                f"{soil_data['potassium_ppm']} ppm",
                f"{soil_data['moisture_percent']}%"
            ],
            "Status": [
                "Optimal" if 6.0 <= soil_data['ph'] <= 7.0 else "Suboptimal",
                "High" if soil_data['nitrogen_ppm'] > 50 else "Medium" if soil_data['nitrogen_ppm'] > 30 else "Low",
                "High" if soil_data['phosphorus_ppm'] > 35 else "Medium" if soil_data['phosphorus_ppm'] > 25 else "Low",
                "High" if soil_data['potassium_ppm'] > 180 else "Medium" if soil_data['potassium_ppm'] > 140 else "Low",
                "Good" if 20 <= soil_data['moisture_percent'] <= 35 else "Poor"
            ]
        }
        
        df_soil = pd.DataFrame(soil_table_data)
        st.dataframe(df_soil, use_container_width=True)
        
        # Fertility metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 Fertility Score", f"{fertility['fertility_score']}/100")
        with col2:
            st.metric("📊 Soil Type", fertility['soil_type'])
        
        # Crop recommendations
        st.markdown("### 🌾 Recommended Crops")
        crop_cols = st.columns(3)
        for i, crop in enumerate(fertility['best_crops'][:6]):
            with crop_cols[i % 3]:
                st.write(f"🌱 {crop}")
                
    except Exception as e:
        st.error(f"Soil Analysis Error: {e}")

def main():
    """Main application function"""
    # Apply custom styling
    apply_custom_styling()
    
    # Create sidebar and get selected page
    page = create_sidebar()
    
    # Page routing
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "🩺 Health & Diagnosis":
        health_diagnosis_page()
    elif page == "📡 Environmental Alerts":
        environmental_alerts_page()

if __name__ == "__main__":
    main()
