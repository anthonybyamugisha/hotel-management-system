#!/usr/bin/env python3
"""
Diagnostic script for Render deployment issues
This script can be run on Render to diagnose common deployment problems
"""

import os
import sys
import json

def check_environment():
    """Check environment variables"""
    print("=== Environment Variables ===")
    important_vars = [
        'RENDER_SERVICE_NAME',
        'RENDER_EXTERNAL_HOSTNAME',
        'DATABASE_URL',
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'PYTHON_VERSION',
        'PORT'
    ]
    
    for var in important_vars:
        value = os.environ.get(var, 'NOT SET')
        if var in ['SECRET_KEY', 'DATABASE_URL'] and value != 'NOT SET':
            print(f"{var}: SET (length: {len(value)})")
        else:
            print(f"{var}: {value}")

def check_files():
    """Check important files"""
    print("\n=== File System Check ===")
    
    important_dirs = [
        '.',
        'hotel_management',
        'reports',
        'reports/sql',
        'static',
        'static/css',
        'staticfiles'
    ]
    
    for directory in important_dirs:
        if os.path.exists(directory):
            try:
                files = os.listdir(directory)
                print(f"{directory}/: {len(files)} items")
                if len(files) <= 10:
                    for f in files:
                        print(f"  - {f}")
            except PermissionError:
                print(f"{directory}/: PERMISSION DENIED")
        else:
            print(f"{directory}/: NOT FOUND")

def check_requirements():
    """Check if requirements are installed"""
    print("\n=== Python Packages ===")
    
    required_packages = [
        'django',
        'gunicorn',
        'dj_database_url',
        'whitenoise',
        'mysqlclient'
    ]
    
    for package in required_packages:
        try:
            if package == 'django':
                import django
                print(f"✓ {package}: {django.get_version()}")
            elif package == 'gunicorn':
                import gunicorn
                print(f"✓ {package}: Installed")
            elif package == 'dj_database_url':
                import dj_database_url
                print(f"✓ {package}: Installed")
            elif package == 'whitenoise':
                import whitenoise
                print(f"✓ {package}: Installed")
            elif package == 'mysqlclient':
                import MySQLdb
                print(f"✓ {package}: Installed")
        except ImportError as e:
            print(f"✗ {package}: NOT INSTALLED ({e})")

def main():
    """Main diagnostic function"""
    print("Hotel Management Application - Render Diagnostics")
    print("=" * 50)
    
    try:
        check_environment()
    except Exception as e:
        print(f"Error checking environment: {e}")
    
    try:
        check_files()
    except Exception as e:
        print(f"Error checking files: {e}")
    
    try:
        check_requirements()
    except Exception as e:
        print(f"Error checking requirements: {e}")
    
    print("\n=== Process Information ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Command line args: {sys.argv}")

if __name__ == "__main__":
    main()