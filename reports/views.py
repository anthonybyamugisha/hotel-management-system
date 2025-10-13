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
