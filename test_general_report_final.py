import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

def test_general_report():
    """Test the general report data fetching"""
    
    # Import the execute_sql function
    from reports.views import execute_sql
    
    try:
        print("Testing general report data fetching...")
        data = execute_sql('general_report.sql')
        
        print(f"Successfully fetched {len(data)} rows")
        if data:
            print("Column names:", list(data[0].keys()))
            print("First row:", data[0])
            print("Last row:", data[-1])
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_general_report()
    if success:
        print("\n✅ General report test completed successfully!")
    else:
        print("\n❌ General report test failed!")