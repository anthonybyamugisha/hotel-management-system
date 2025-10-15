import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

def debug_general_report():
    """Debug the general report data fetching"""
    
    # Import Django database connection
    from django.db import connection
    import os
    
    # Path to the general report SQL file
    path = os.path.join('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management', 'reports', 'sql', 'general_report.sql')
    
    try:
        # Read the SQL file
        with open(path, 'r', encoding='utf-8') as file:
            query = file.read()
        
        print("SQL file content length:", len(query))
        print("First 200 characters:", query[:200])
        
        # Split the queries by semicolon
        queries = [q.strip() for q in query.split(';') if q.strip()]
        
        # Filter for SELECT queries
        select_queries = []
        for q in queries:
            # Check if this query starts with SELECT (ignoring comments)
            lines = q.strip().split('\n')
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('--'):
                    if stripped_line.upper().startswith('SELECT'):
                        select_queries.append(q)
                        break
        
        print(f"\nFound {len(select_queries)} SELECT queries:")
        for i, q in enumerate(select_queries):
            print(f"Query {i+1}: {q[:100]}...")
        
        # Execute each query and collect results
        all_data = []
        section_names = [
            'hotels_and_staff',
            'guests_and_bookings', 
            'room_status_summary',
            'payments_per_booking',
            'invoices_outstanding',
            'services_used',
            'total_payments_per_guest',
            'services_revenue',
            'booking_status_summary',
            'hotel_revenue_summary'
        ]
        
        with connection.cursor() as cursor:
            for i, single_query in enumerate(select_queries):
                try:
                    print(f"\n--- Executing Query {i+1} ({section_names[i] if i < len(section_names) else 'unknown'}) ---")
                    print("Query:", single_query[:200] + "..." if len(single_query) > 200 else single_query)
                    cursor.execute(single_query)
                    columns = [col[0] for col in cursor.description]
                    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    
                    print(f"Columns: {columns}")
                    print(f"Rows returned: {len(data)}")
                    if data:
                        print("First row:", data[0])
                    
                    section_name = section_names[i] if i < len(section_names) else f'section_{i}'
                    all_data.append({
                        'section_name': section_name,
                        'columns': columns,
                        'data': data
                    })
                except Exception as e:
                    print(f"Error executing query {i+1}: {e}")
                    print("Query:", single_query[:200])
                    return False
        
        print(f"\n✅ Successfully processed {len(all_data)} sections")
        for section in all_data:
            print(f"- {section['section_name']}: {len(section['data'])} rows")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Debugging general report data fetching...")
    success = debug_general_report()
    if success:
        print("\n🎉 Debug completed successfully!")
    else:
        print("\n❌ Debug failed!")