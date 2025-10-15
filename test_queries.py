import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

def test_general_report_queries():
    """Test that all queries in the general report can be executed successfully"""
    
    # Path to the general report SQL file
    sql_file_path = 'c:\\Users\\byamu\\Desktop\\Database M\\Hotel Management\\reports\\sql\\general_report.sql'
    
    try:
        # Read the SQL file
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split queries by semicolon
        queries = [q.strip() for q in sql_content.split(';') if q.strip() and q.upper().startswith('SELECT')]
        
        print(f"Found {len(queries)} SELECT queries in the general report SQL file")
        
        # Import Django database connection
        from django.db import connection
        
        # Execute each query
        with connection.cursor() as cursor:
            for i, query in enumerate(queries):
                try:
                    print(f"\nExecuting query {i+1}...")
                    print(f"Query: {query[:100]}...")
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    print(f"Query {i+1} executed successfully.")
                    print(f"Columns: {columns}")
                    print(f"Returned {len(rows)} rows")
                    if rows:
                        print(f"First row: {rows[0]}")
                except Exception as e:
                    print(f"Error executing query {i+1}: {e}")
                    print(f"Query content: {query[:200]}...")
                    return False
        
        print("\n✅ All queries executed successfully!")
        return True
        
    except Exception as e:
        print(f"Error reading or processing SQL file: {e}")
        return False

if __name__ == "__main__":
    print("Testing general report queries...")
    success = test_general_report_queries()
    if success:
        print("\n🎉 All tests passed! Your data should be displayed correctly in the general report.")
    else:
        print("\n❌ Some tests failed!")