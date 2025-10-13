import os
import django
from django.conf import settings
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

# Import the execute_sql function
import sys
sys.path.append('.')
from reports.views import execute_sql

try:
    # Test all_rooms.sql
    print("Testing all_rooms.sql...")
    all_rooms = execute_sql('all_rooms.sql')
    print(f"Found {len(all_rooms)} rooms")
    if all_rooms:
        print("First room:", all_rooms[0])
    
    # Test room_availability.sql
    print("\nTesting room_availability.sql...")
    room_availability = execute_sql('room_availability.sql')
    print(f"Found {len(room_availability)} availability records")
    if room_availability:
        print("First availability record:", room_availability[0])
    
    # Test room_status_details.sql
    print("\nTesting room_status_details.sql...")
    room_status = execute_sql('room_status_details.sql')
    print(f"Found {len(room_status)} status records")
    if room_status:
        print("First status record:", room_status[0])
    
    # Test room_utilization.sql
    print("\nTesting room_utilization.sql...")
    room_utilization = execute_sql('room_utilization.sql')
    print(f"Found {len(room_utilization)} utilization records")
    if room_utilization:
        print("First utilization record:", room_utilization[0])
    
    # Test hotels_list.sql
    print("\nTesting hotels_list.sql...")
    hotels = execute_sql('hotels_list.sql')
    print(f"Found {len(hotels)} hotels")
    if hotels:
        print("First hotel:", hotels[0])
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()