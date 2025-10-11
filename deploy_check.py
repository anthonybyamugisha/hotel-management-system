#!/usr/bin/env python3
"""
Deployment verification script for Hotel Management System
"""

import os
from pathlib import Path

def check_file_exists(filename):
    """Check if a file exists in the current directory"""
    file_path = Path(filename)
    if file_path.exists():
        print(f"✓ {filename} found")
        return True
    else:
        print(f"✗ {filename} NOT FOUND")
        return False

def check_requirements_content():
    """Check if requirements.txt has the expected content"""
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            required_packages = [
                "Django==5.2.7",
                "mysqlclient==2.2.4",
                "gunicorn==22.0.0",
                "python-decouple==3.8",
                "dj-database-url==2.1.0",
                "whitenoise==6.6.0"
            ]
            
            missing_packages = []
            for package in required_packages:
                if package not in content:
                    missing_packages.append(package)
            
            if not missing_packages:
                print("✓ requirements.txt has all required packages")
                return True
            else:
                print(f"✗ Missing packages in requirements.txt: {', '.join(missing_packages)}")
                return False
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False

def check_procfile_content():
    """Check if Procfile has the correct content"""
    try:
        with open("Procfile", "r") as f:
            content = f.read().strip()
            expected_content = "web: gunicorn hotel_management.wsgi:application"
            
            if content == expected_content:
                print("✓ Procfile has correct content")
                return True
            else:
                print(f"✗ Procfile content incorrect. Expected: {expected_content}, Got: {content}")
                return False
    except Exception as e:
        print(f"✗ Error reading Procfile: {e}")
        return False

def main():
    """Main verification function"""
    print("Hotel Management System - Deployment Verification")
    print("=" * 50)
    
    # List of required files
    required_files = [
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "render.yaml"
    ]
    
    # Check if all required files exist
    all_files_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_files_exist = False
    
    print()
    
    # Check content of specific files
    requirements_ok = check_requirements_content()
    procfile_ok = check_procfile_content()
    
    print()
    
    # Final assessment
    if all_files_exist and requirements_ok and procfile_ok:
        print("🎉 All deployment files are correctly set up!")
        print("\nNext steps:")
        print("1. Commit these files to your repository")
        print("2. Connect your repository to Render")
        print("3. Set up environment variables on Render")
        print("4. Deploy your application")
    else:
        print("❌ Some deployment files are missing or incorrect.")
        print("Please fix the issues above before deploying.")

if __name__ == "__main__":
    main()