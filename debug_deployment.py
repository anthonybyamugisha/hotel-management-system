#!/usr/bin/env python3
"""
Deployment Debugging Script for Hotel Management Application
This script helps identify common deployment issues with the Hotel Management app on Render.
"""

import os
import sys
import subprocess
import json

def check_environment_variables():
    """Check if required environment variables are set"""
    print("=== Checking Environment Variables ===")
    
    required_vars = ['DATABASE_URL', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: SET (length: {len(value)})")
        else:
            print(f"✗ {var}: NOT SET")
            missing_vars.append(var)
    
    # Check optional vars
    optional_vars = ['DEBUG', 'ALLOWED_HOSTS']
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: {value}")
        else:
            print(f"○ {var}: Not set (using defaults)")
    
    return len(missing_vars) == 0

def check_python_requirements():
    """Check if all required packages are installed"""
    print("\n=== Checking Python Requirements ===")
    
    try:
        import django
        print(f"✓ Django: {django.get_version()}")
    except ImportError:
        print("✗ Django: NOT INSTALLED")
        return False
    
    try:
        import mysql.connector
        print("✓ mysql-connector-python: INSTALLED")
    except ImportError:
        print("○ mysql-connector-python: NOT INSTALLED (may not be needed)")
    
    try:
        import dj_database_url
        print("✓ dj-database-url: INSTALLED")
    except ImportError:
        print("✗ dj-database-url: NOT INSTALLED")
        return False
        
    try:
        import whitenoise
        print("✓ whitenoise: INSTALLED")
    except ImportError:
        print("✗ whitenoise: NOT INSTALLED")
        return False
        
    return True

def check_django_settings():
    """Check Django settings configuration"""
    print("\n=== Checking Django Settings ===")
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
    
    try:
        import django
        from django.conf import settings
        django.setup()
        
        print(f"✓ Django settings loaded successfully")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"  STATIC_URL: {settings.STATIC_URL}")
        
        # Check database configuration
        db_config = settings.DATABASES.get('default', {})
        print(f"  Database ENGINE: {db_config.get('ENGINE', 'NOT SET')}")
        if 'sqlite' in db_config.get('ENGINE', ''):
            print("  ○ Using SQLite database (development mode)")
        else:
            print("  ○ Using external database")
            
        return True
    except Exception as e:
        print(f"✗ Error loading Django settings: {e}")
        return False

def check_static_files():
    """Check if static files are properly configured"""
    print("\n=== Checking Static Files ===")
    
    static_root = os.path.join(os.getcwd(), 'staticfiles')
    static_dir = os.path.join(os.getcwd(), 'static')
    
    print(f"  Static root directory: {static_root}")
    print(f"  Static source directory: {static_dir}")
    
    if os.path.exists(static_root):
        files = os.listdir(static_root)
        print(f"✓ Static root exists with {len(files)} items")
    else:
        print("○ Static root directory doesn't exist yet (will be created during collectstatic)")
        
    if os.path.exists(static_dir):
        files = os.listdir(static_dir)
        print(f"✓ Static source directory exists with {len(files)} items")
        if 'css' in files:
            css_files = os.listdir(os.path.join(static_dir, 'css'))
            print(f"  CSS directory has {len(css_files)} files")
    else:
        print("✗ Static source directory missing")
        return False
        
    return True

def check_render_config():
    """Check Render configuration files"""
    print("\n=== Checking Render Configuration ===")
    
    files_to_check = ['Procfile', 'runtime.txt', 'render.yaml']
    
    for file_name in files_to_check:
        if os.path.exists(file_name):
            print(f"✓ {file_name}: EXISTS")
        else:
            print(f"✗ {file_name}: MISSING")
            
    # Check Procfile content
    if os.path.exists('Procfile'):
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            print(f"  Procfile content: {content}")
            
    return True

def main():
    """Main debugging function"""
    print("Hotel Management Application Deployment Debugger")
    print("=" * 50)
    
    checks = [
        check_environment_variables,
        check_python_requirements,
        check_django_settings,
        check_static_files,
        check_render_config
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"Error during {check.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("✓ All checks passed! Application should deploy correctly.")
        print("\nNext steps:")
        print("1. Ensure your Render environment variables are set correctly")
        print("2. Check Render logs for any runtime errors")
        print("3. Verify database connection if using external database")
    else:
        print("✗ Some checks failed. Please review the issues above.")
        print("\nCommon fixes:")
        print("1. Check that all required environment variables are set in Render")
        print("2. Verify requirements.txt includes all necessary packages")
        print("3. Ensure static files are collected properly")
        print("4. Check database connection settings")

if __name__ == "__main__":
    main()