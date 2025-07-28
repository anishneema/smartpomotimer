#!/usr/bin/env python3
"""
Launcher script for Focus Flow Agent Web App
"""

import subprocess
import sys
import os

def main():
    print("🎯 Starting Focus Flow Agent Web App...")
    print("📱 Opening browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app")
    print()
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Focus Flow Agent Web App stopped.")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("Make sure you have installed all dependencies: pip3 install -r requirements.txt")

if __name__ == "__main__":
    main() 