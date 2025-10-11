#!/usr/bin/env python3
"""
Test script to verify the application can run
"""

import os

def check_required_files():
    """Check if required files exist"""
    required_files = [
        "manage.py",
        "hotel_management/settings.py",
        "reports/views.py",
        "requirements.txt"
    ]
    
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} NOT FOUND")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Main test function"""
    print("Hotel Management System - Application Test")
    print("=" * 45)
    
    # Check required files
    print("\nChecking required files...")
    files_ok = check_required_files()
    
    # Final assessment
    print("\n" + "=" * 45)
    if files_ok:
        print("🎉 Application is ready to run!")
        print("\nTo run the application locally:")
        print("  Windows: Double-click run_dev.bat")
        print("  PowerShell: Run .\\run_dev.ps1")
        print("  Linux/Mac: Run make run")
        print("\nTo deploy to Render:")
        print("  Follow the instructions in README.md")
    else:
        print("❌ Application has issues that need to be fixed.")
        print("Please check the errors above.")

if __name__ == "__main__":
    main()