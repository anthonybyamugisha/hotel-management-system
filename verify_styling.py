#!/usr/bin/env python3
"""
Verification script to check if all templates have proper styling
"""

import os
from pathlib import Path

def check_template_styling(template_path):
    """Check if a template has proper styling"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it has either inline styles or links to CSS
        has_inline_styles = '<style>' in content
        has_css_link = 'href="{% static \'css/styles.css' in content or 'href="/static/css/styles.css' in content
        
        if has_inline_styles or has_css_link:
            print(f"✓ {template_path.name} has styling")
            return True
        else:
            print(f"✗ {template_path.name} missing styling")
            return False
    except Exception as e:
        print(f"✗ Error checking {template_path.name}: {e}")
        return False

def main():
    """Main verification function"""
    print("Hotel Management System - Styling Verification")
    print("=" * 50)
    
    # Define template directory
    templates_dir = Path("reports/templates/reports")
    
    if not templates_dir.exists():
        print("✗ Templates directory not found")
        return
    
    # Check all HTML templates
    templates = list(templates_dir.glob("*.html"))
    
    if not templates:
        print("✗ No HTML templates found")
        return
    
    all_styled = True
    for template in templates:
        if not check_template_styling(template):
            all_styled = False
    
    print("\n" + "=" * 50)
    if all_styled:
        print("🎉 All templates have proper styling!")
    else:
        print("❌ Some templates are missing styling.")

if __name__ == "__main__":
    main()