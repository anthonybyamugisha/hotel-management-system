import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

def test_chart_queries():
    """Test all chart queries used in the dashboard"""
    
    # Import the execute_sql function
    from reports.views import execute_sql
    
    # List of chart SQL files to test
    chart_files = [
        'monthly_revenue_collection.sql',
        'hotel_occupancy_rates.sql', 
        'room_type_distribution.sql',
        'department_performance.sql'
    ]
    
    results = {}
    
    for file_name in chart_files:
        try:
            print(f"\n{'='*50}")
            print(f"Testing {file_name}...")
            data = execute_sql(file_name)
            
            results[file_name] = {
                'success': True,
                'row_count': len(data),
                'columns': list(data[0].keys()) if data else [],
                'sample_data': data[:3] if data else []
            }
            
            print(f"✅ SUCCESS: Fetched {len(data)} rows")
            print(f"Columns: {list(data[0].keys()) if data else 'None'}")
            if data:
                print("Sample data:")
                for i, row in enumerate(data[:3]):
                    print(f"  {i+1}. {row}")
                    
        except Exception as e:
            print(f"❌ ERROR in {file_name}: {e}")
            results[file_name] = {
                'success': False,
                'error': str(e)
            }
            import traceback
            traceback.print_exc()
    
    # Print summary
    print(f"\n{'='*50}")
    print("SUMMARY REPORT")
    print(f"{'='*50}")
    
    for file_name, result in results.items():
        if result['success']:
            print(f"✅ {file_name}: {result['row_count']} rows")
        else:
            print(f"❌ {file_name}: FAILED - {result['error']}")
    
    return all(result['success'] for result in results.values())

if __name__ == "__main__":
    print("Testing all dashboard chart queries...")
    success = test_chart_queries()
    if success:
        print("\n🎉 All chart queries executed successfully!")
    else:
        print("\n💥 Some chart queries failed!")