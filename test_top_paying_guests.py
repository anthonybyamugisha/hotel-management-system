import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

def test_top_paying_guests():
    """Test the top paying guests report data fetching"""
    
    # Import the execute_sql function
    from reports.views import execute_sql
    
    try:
        print("Testing top paying guests report data fetching...")
        data = execute_sql('top_paying_guests.sql')
        
        print(f"Successfully fetched {len(data)} rows")
        if data:
            print("Column names:", list(data[0].keys()))
            print("Sample rows:")
            for i, row in enumerate(data[:10]):  # Show first 10 rows
                print(f"  {i+1}. {row}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_top_paying_guests()
    if success:
        print("\n✅ Top paying guests report test completed successfully!")
    else:
        print("\n❌ Top paying guests report test failed!")