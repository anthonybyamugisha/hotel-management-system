from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.exceptions import ImproperlyConfigured
import os
import json
from collections import defaultdict

# Helper function to read and execute SQL files
def execute_sql(file_name):
    path = os.path.join(os.path.dirname(__file__), 'sql', file_name)
    # Try multiple encoding options
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    query = None
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as file:
                query = file.read()
            break
        except UnicodeDecodeError:
            continue
    
    if query is None:
        # If all encodings fail, try with error handling
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            query = file.read()
    
    # For SQL files with multiple queries, we need to find the main one
    # Look for queries that start with SELECT
    queries = [q.strip() for q in query.split(';') if q.strip()]
    if queries:
        # Use the last query that starts with SELECT (typically the main report query)
        select_queries = [q for q in queries if q.upper().startswith('SELECT')]
        if select_queries:
            query = select_queries[-1]
        else:
            # If no SELECT queries, use the last query
            query = queries[-1]
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return data

# Create your views here.
def index(request):
    return render(request, 'reports/index.html')


def reports_index(request):
    return render(request, 'reports/reports_index.html')


def dashboard(request):
    return render(request, 'reports/dashboard.html')


def chart_data(request):
    try:
        # Get data for all charts
        revenue_data = execute_sql('monthly_revenue_collection.sql')
        occupancy_data = execute_sql('hotel_occupancy_rates.sql')  # Use the new file
        room_type_data_rows = execute_sql('room_type_distribution.sql')
        department_performance_data = execute_sql('department_performance.sql')
        
        # Debug: Print data to console
        print("Revenue data:", revenue_data)
        print("Occupancy data:", occupancy_data)
        print("Room type data:", room_type_data_rows)
        print("Department performance data:", department_performance_data)
        
        # Process revenue data
        revenue_chart_data = {
            'labels': [],
            'room_revenue': [],
            'service_revenue': []
        }
        
        print("Processing revenue data...")
        print("Revenue data rows:", revenue_data)
        
        # Group revenue data by month
        monthly_data = {}
        for row in revenue_data:
            month = row.get('Month', '')
            room_rev = float(row.get('Total_Room_Revenue', 0) or 0)
            service_rev = float(row.get('Total_Service_Revenue', 0) or 0)
            
            print(f"Month: {month}, Room Rev: {room_rev}, Service Rev: {service_rev}")
            
            if month:
                if month not in monthly_data:
                    monthly_data[month] = {'room': 0, 'service': 0}
                monthly_data[month]['room'] += room_rev
                monthly_data[month]['service'] += service_rev
        
        # Sort by month and prepare chart data
        sorted_months = sorted(monthly_data.keys())
        revenue_chart_data['labels'] = sorted_months
        revenue_chart_data['room_revenue'] = [monthly_data[month]['room'] for month in sorted_months]
        revenue_chart_data['service_revenue'] = [monthly_data[month]['service'] for month in sorted_months]
        
        print("Final revenue chart data:", revenue_chart_data)
        
        # Process occupancy data
        occupancy_chart_data = {
            'hotels': [],
            'rates': []
        }
        
        print("Processing occupancy data...")
        print("Occupancy data rows:", occupancy_data)
        
        for row in occupancy_data:
            hotel = row.get('Hotel_Name', '')
            rate = float(row.get('Occupancy_Rate', 0) or 0)
            
            print(f"Hotel: {hotel}, Rate: {rate}")
            
            if hotel and rate is not None:
                occupancy_chart_data['hotels'].append(hotel)
                occupancy_chart_data['rates'].append(rate)
        
        print("Final occupancy chart data:", occupancy_chart_data)
        
        # Process room type data
        room_type_data = {
            'types': [],
            'counts': []
        }
        
        print("Processing room type data...")
        print("Room type data rows:", room_type_data_rows)
        
        for row in room_type_data_rows:
            room_type = row.get('room_type', '')
            room_count = int(row.get('room_count', 0))
            
            print(f"Room Type: {room_type}, Count: {room_count}")
            
            if room_type:
                room_type_data['types'].append(room_type)
                room_type_data['counts'].append(room_count)
        
        print("Final room type chart data:", room_type_data)
        
        # Process department performance data
        staff_chart_data = {
            'departments': [],
            'scores': []
        }
        
        print("Processing department performance data...")
        print("Department performance data rows:", department_performance_data)
        
        for row in department_performance_data:
            dept = row.get('department', '')
            score = float(row.get('performance_score', 0) or 0)
            
            print(f"Department: {dept}, Score: {score}")
            
            if dept:
                staff_chart_data['departments'].append(dept)
                staff_chart_data['scores'].append(score)
        
        print("Final staff chart data:", staff_chart_data)
        
        chart_data = {
            'revenue': revenue_chart_data,
            'occupancy': occupancy_chart_data,
            'staff': staff_chart_data,
            'room_types': room_type_data
        }
        
        print("Final chart data:", chart_data)
        
        return JsonResponse(chart_data)
        
    except Exception as e:
        # Log the error
        print(f"Error in chart_data view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Return error data so we can see what's happening
        error_data = {
            'error': str(e),
            'revenue': {'labels': [], 'room_revenue': [], 'service_revenue': []},
            'occupancy': {'hotels': [], 'rates': []},
            'staff': {'departments': [], 'scores': []},
            'room_types': {'types': [], 'counts': []}
        }
        return JsonResponse(error_data)


def general_report(request):
    try:
        data = execute_sql('general_report.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/general_report.html', context)


def room_occupancy_report(request):
    try:
        data = execute_sql('room_occupancy_report.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/room_occupancy_report.html', context)


def staff_performance(request):
    try:
        data = execute_sql('staff_performance.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/staff_performance.html', context)


def monthly_revenue_collection(request):
    try:
        data = execute_sql('monthly_revenue_collection.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/monthly_revenue_collection.html', context)


def outstanding_payments_per_guest(request):
    try:
        data = execute_sql('outstanding_payments_per_guest.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/outstanding_payments_per_guest.html', context)


def top_paying_guests(request):
    try:
        data = execute_sql('top_paying_guests.sql')
        context = {'data': data}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/top_paying_guests.html', context)


def test_database_connection(request):
    """
    Simple test view to check database connection and data
    """
    try:
        # Test basic database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM hotel")
            hotel_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM room")
            room_count = cursor.fetchone()[0]
            
            # Test occupancy rate query
            cursor.execute("""
                SELECT
                    h.hotel_name,
                    ROUND(
                        (SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
                    ) AS occupancy_rate
                FROM room r
                JOIN hotel h ON r.hotel_id = h.hotel_id
                GROUP BY h.hotel_name
                ORDER BY occupancy_rate DESC
            """)
            occupancy_data = cursor.fetchall()
            
        context = {
            'hotel_count': hotel_count,
            'room_count': room_count,
            'occupancy_data': occupancy_data,
            'status': 'success'
        }
    except Exception as e:
        context = {
            'status': 'error',
            'error_message': str(e)
        }
    
    return JsonResponse(context)

def hotels_and_staff(request):
    try:
        data = execute_sql('hotels_and_staff.sql')
        
        # Process data to group staff by hotel
        hotels = []
        current_hotel = None
        current_hotel_data = None
        
        for row in data:
            # Check if this is a new hotel
            if current_hotel != row['hotel_id']:
                # If we were processing a hotel, add it to the list
                if current_hotel_data:
                    hotels.append(current_hotel_data)
                
                # Start a new hotel
                current_hotel = row['hotel_id']
                current_hotel_data = {
                    'hotel_id': row['hotel_id'],
                    'hotel_name': row['hotel_name'],
                    'location': row['location'],
                    'hotel_contact': row['hotel_contact'],
                    'staff_members': []
                }
            
            # Add staff member if exists
            if row['staff_id'] is not None and current_hotel_data is not None:
                current_hotel_data['staff_members'].append({
                    'staff_id': row['staff_id'],
                    'staff_name': row['staff_name'],
                    'staff_role': row['staff_role'],
                    'staff_contact': row['staff_contact']
                })
        
        # Don't forget the last hotel
        if current_hotel_data:
            hotels.append(current_hotel_data)
        
        context = {'hotels': hotels}
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'reports/hotels_and_staff.html', context)


def room_management(request):
    try:
        # Get filter parameters from the request
        hotel_id = request.GET.get('hotel_id', '')
        room_status = request.GET.get('room_status', '')
        room_type = request.GET.get('room_type', '')
        
        # Build dynamic SQL query based on filters
        with connection.cursor() as cursor:
            # All rooms query with filters
            all_rooms_query = """
                SELECT 
                    r.room_id,
                    r.room_type,
                    r.room_status,
                    h.hotel_name,
                    h.hotel_id
                FROM room r
                JOIN hotel h ON r.hotel_id = h.hotel_id
                WHERE 1=1
            """
            
            params = []
            if hotel_id:
                all_rooms_query += " AND h.hotel_id = %s"
                params.append(hotel_id)
            if room_status:
                all_rooms_query += " AND r.room_status = %s"
                params.append(room_status)
            if room_type:
                all_rooms_query += " AND r.room_type = %s"
                params.append(room_type)
                
            all_rooms_query += " ORDER BY h.hotel_name, r.room_id"
            
            cursor.execute(all_rooms_query, params)
            columns = [col[0] for col in cursor.description]
            all_rooms = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Room availability query (no filters needed for this view)
            cursor.execute("""
                SELECT 
                    h.hotel_name,
                    r.room_type,
                    COUNT(r.room_id) AS total_rooms,
                    SUM(CASE WHEN r.room_status = 'Available' THEN 1 ELSE 0 END) AS available_rooms,
                    SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
                    SUM(CASE WHEN r.room_status = 'Booked' THEN 1 ELSE 0 END) AS booked_rooms,
                    SUM(CASE WHEN r.room_status = 'Maintenance' THEN 1 ELSE 0 END) AS maintenance_rooms
                FROM room r
                JOIN hotel h ON r.hotel_id = h.hotel_id
                GROUP BY h.hotel_name, r.room_type
                ORDER BY h.hotel_name, r.room_type
            """)
            columns = [col[0] for col in cursor.description]
            room_availability = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Room status details query with filters
            status_query = """
                SELECT 
                    h.hotel_name,
                    r.room_id,
                    r.room_type,
                    r.room_status,
                    b.booking_id,
                    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
                    b.check_in_date,
                    b.check_out_date
                FROM room r
                JOIN hotel h ON r.hotel_id = h.hotel_id
                LEFT JOIN booking b ON r.room_id = b.room_id AND b.booking_status = 'Confirmed'
                LEFT JOIN guest g ON b.guest_id = g.guest_id
                WHERE 1=1
            """
            
            status_params = []
            if hotel_id:
                status_query += " AND h.hotel_id = %s"
                status_params.append(hotel_id)
            if room_status:
                status_query += " AND r.room_status = %s"
                status_params.append(room_status)
            if room_type:
                status_query += " AND r.room_type = %s"
                status_params.append(room_type)
                
            status_query += " ORDER BY h.hotel_name, r.room_id"
            
            cursor.execute(status_query, status_params)
            columns = [col[0] for col in cursor.description]
            room_status_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Room utilization query (no filters needed for this view)
            cursor.execute("""
                SELECT
                    h.hotel_name,
                    COUNT(r.room_id) AS total_rooms,
                    ROUND(
                        (SUM(CASE WHEN r.room_status IN ('Occupied', 'Booked') THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
                    ) AS utilization_rate_percent
                FROM room r
                JOIN hotel h ON r.hotel_id = h.hotel_id
                GROUP BY h.hotel_name
                ORDER BY utilization_rate_percent DESC
            """)
            columns = [col[0] for col in cursor.description]
            room_utilization = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Hotels for filter dropdown (no filters needed for this view)
            cursor.execute("""
                SELECT DISTINCT h.hotel_id, h.hotel_name
                FROM hotel h
                JOIN room r ON h.hotel_id = r.hotel_id
                ORDER BY h.hotel_name
            """)
            columns = [col[0] for col in cursor.description]
            hotels = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        context = {
            'all_rooms': all_rooms,
            'room_availability': room_availability,
            'room_status': room_status_data,
            'room_utilization': room_utilization,
            'hotels': hotels,
            'filter_hotel_id': hotel_id,
            'filter_room_status': room_status,
            'filter_room_type': room_type
        }
    except Exception as e:
        print("Error in room_management view:", str(e))
        import traceback
        traceback.print_exc()
        context = {'error': str(e)}
    
    return render(request, 'reports/room_management.html', context)


def update_room_status(request):
    if request.method == 'POST':
        try:
            room_id = request.POST.get('room_id')
            status = request.POST.get('status')
            
            # Validate inputs
            if not room_id or not status:
                return JsonResponse({'success': False, 'error': 'Missing room_id or status'})
            
            # Validate status is one of the allowed values
            allowed_statuses = ['Available', 'Occupied', 'Booked', 'Maintenance']
            if status not in allowed_statuses:
                return JsonResponse({'success': False, 'error': 'Invalid status'})
            
            # Update the room status in the database
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE room SET room_status = %s WHERE room_id = %s",
                    [status, room_id]
                )
            
            return JsonResponse({'success': True, 'message': f'Room {room_id} status updated to {status}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
