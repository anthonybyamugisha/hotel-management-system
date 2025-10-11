#!/usr/bin/env python3
"""
Simple test script to verify Django application deployment
"""

import os
import sys
import django
from django.conf import settings

def test_django_setup():
    """Test if Django can be properly configured"""
    print("Testing Django setup...")
    
    try:
        # Set the Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
        
        # Setup Django
        django.setup()
        
        print("✓ Django setup successful")
        print(f"  Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"  Debug mode: {settings.DEBUG}")
        print(f"  Allowed hosts: {settings.ALLOWED_HOSTS}")
        
        # Test database configuration
        db_config = settings.DATABASES.get('default', {})
        print(f"  Database engine: {db_config.get('ENGINE', 'NOT SET')}")
        
        return True
    except Exception as e:
        print(f"✗ Django setup failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: SET")
        else:
            print(f"○ {var}: NOT SET (may be set by Render)")
    
    # Check Render-specific variables
    render_vars = ['RENDER_SERVICE_NAME', 'RENDER_EXTERNAL_HOSTNAME']
    for var in render_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: {value}")
    
    return True

def main():
    """Main test function"""
    print("Hotel Management Application Deployment Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_django_setup
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Error during {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("✓ All tests passed! Application should work correctly.")
    else:
        print("✗ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()