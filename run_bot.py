"""
SneakerBot Ultimate - Main Entry Point
Run this to start the application
"""
import subprocess
import sys
import os

def main():
    """Main entry point"""
    print("=" * 60)
    print("  SneakerBot Ultimate - Security Research Project")
    print("=" * 60)
    print()
    print("Starting GUI...")
    print()
    
    # Run the GUI
    try:
        subprocess.run([sys.executable, "gui/main.py"])
    except KeyboardInterrupt:
        print("\nShutdown requested... exiting")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
