"""
Streamlit App Launcher
Simple script to run the farming management system
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    print("🌾 Starting Farming Management System...")
    print("📱 Opening web application in your browser...")
    
    # Get the directory where this script is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(app_dir, "app.py")
    
    try:
        # Run streamlit with the app
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first:")
        print("   pip install streamlit")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
