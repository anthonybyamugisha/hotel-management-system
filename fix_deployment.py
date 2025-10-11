#!/usr/bin/env python3
"""
Deployment Fix Script for Hotel Management Application
This script applies common fixes for deployment issues on Render.
"""

import os
import sys
import subprocess
import shutil

def fix_settings_py():
    """Fix settings.py for better Render deployment compatibility"""
    settings_path = 'hotel_management/settings.py'
    
    if not os.path.exists(settings_path):
        print("✗ settings.py not found")
        return False
        
    try:
        with open(settings_path, 'r') as f:
            content = f.read()
            
        # Ensure proper host configuration
        if 'ALLOWED_HOSTS = os.environ.get(\'ALLOWED_HOSTS\'' in content:
            print("✓ ALLOWED_HOSTS already configured for Render")
        else:
            # Add Render-specific ALLOWED_HOSTS
            content = content.replace(
                "ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')",
                "ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,your-app-name.onrender.com').split(',')"
            )
            print("✓ Updated ALLOWED_HOSTS for Render")
            
        # Ensure proper static files configuration
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in content:
            print("✓ WhiteNoise middleware already configured")
        else:
            print("✗ WhiteNoise middleware not found")
            
        with open(settings_path, 'w') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"✗ Error fixing settings.py: {e}")
        return False

def fix_requirements_txt():
    """Ensure requirements.txt has all necessary packages"""
    req_path = 'requirements.txt'
    
    required_packages = [
        'Django==5.2.7',
        'mysqlclient==2.2.4',
        'gunicorn==22.0.0',
        'python-decouple==3.8',
        'dj-database-url==2.1.0',
        'whitenoise==6.6.0'
    ]
    
    try:
        if not os.path.exists(req_path):
            with open(req_path, 'w') as f:
                for package in required_packages:
                    f.write(f"{package}\n")
            print("✓ Created requirements.txt with all required packages")
            return True
            
        with open(req_path, 'r') as f:
            content = f.read()
            
        missing_packages = []
        for package in required_packages:
            if package.split('==')[0] not in content:
                missing_packages.append(package)
                
        if missing_packages:
            with open(req_path, 'a') as f:
                f.write('\n')  # Add newline if needed
                for package in missing_packages:
                    f.write(f"{package}\n")
            print(f"✓ Added missing packages to requirements.txt: {missing_packages}")
        else:
            print("✓ All required packages present in requirements.txt")
            
        return True
    except Exception as e:
        print(f"✗ Error fixing requirements.txt: {e}")
        return False

def fix_procfile():
    """Ensure Procfile is correctly configured"""
    procfile_path = 'Procfile'
    
    try:
        correct_content = "web: gunicorn hotel_management.wsgi:application"
        
        if not os.path.exists(procfile_path):
            with open(procfile_path, 'w') as f:
                f.write(correct_content)
            print("✓ Created Procfile with correct configuration")
            return True
            
        with open(procfile_path, 'r') as f:
            content = f.read().strip()
            
        if content == correct_content:
            print("✓ Procfile already correctly configured")
            return True
        else:
            with open(procfile_path, 'w') as f:
                f.write(correct_content)
            print("✓ Fixed Procfile configuration")
            return True
            
    except Exception as e:
        print(f"✗ Error fixing Procfile: {e}")
        return False

def collect_static_files():
    """Run collectstatic command"""
    print("=== Collecting Static Files ===")
    
    try:
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
        
        # Run collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Static files collected successfully")
            print(result.stdout)
            return True
        else:
            print("✗ Error collecting static files:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error running collectstatic: {e}")
        return False

def main():
    """Main fix function"""
    print("Hotel Management Application Deployment Fixer")
    print("=" * 50)
    
    fixes = [
        ("Fixing settings.py", fix_settings_py),
        ("Fixing requirements.txt", fix_requirements_txt),
        ("Fixing Procfile", fix_procfile),
        ("Collecting static files", collect_static_files)
    ]
    
    results = []
    for name, fix_func in fixes:
        print(f"\n{name}")
        print("-" * len(name))
        try:
            result = fix_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Error during {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("FIX SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("✓ All fixes applied successfully!")
        print("\nNext steps:")
        print("1. Commit these changes to your repository")
        print("2. Redeploy to Render")
        print("3. Check Render logs if issues persist")
    else:
        failed_count = len([r for r in results if not r])
        print(f"✗ {failed_count} fixes failed. Please review the errors above.")

if __name__ == "__main__":
    main()