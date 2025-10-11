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
        occupancy_data = execute_sql('room_occupancy_report.sql')
        staff_data = execute_sql('staff_performance.sql')
        
        # Process revenue data
        revenue_chart_data = {
            'labels': [],
            'room_revenue': [],
            'service_revenue': []
        }
        
        # Group revenue data by month
        monthly_data = {}
        for row in revenue_data:
            month = row.get('Month', row.get('month', ''))
            room_rev = float(row.get('Total_Room_Revenue', row.get('total_room_revenue', 0)) or 0)
            service_rev = float(row.get('Total_Service_Revenue', row.get('total_service_revenue', 0)) or 0)
            
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
        
        # Process occupancy data
        occupancy_chart_data = {
            'hotels': [],
            'rates': []
        }
        
        for row in occupancy_data:
            hotel = row.get('Hotel_Name', row.get('hotel_name', ''))
            rate = float(row.get('Occupancy_Rate', row.get('occupancy_rate', 0)) or 0)
            
            if hotel and rate is not None:
                occupancy_chart_data['hotels'].append(hotel)
                occupancy_chart_data['rates'].append(rate)
        
        # Process staff data
        staff_chart_data = {
            'departments': [],
            'scores': []
        }
        
        for row in staff_data:
            dept = row.get('Department', row.get('department', ''))
            score = float(row.get('Avg_Score', row.get('avg_score', 0)) or 0)
            
            if dept and score is not None:
                staff_chart_data['departments'].append(dept)
                staff_chart_data['scores'].append(score)
        
        # Room type distribution (static data for now)
        room_type_data = {
            'types': ['Single', 'Double', 'Suite', 'Deluxe', 'Presidential'],
            'counts': [30, 45, 15, 8, 2]
        }
        
        chart_data = {
            'revenue': revenue_chart_data,
            'occupancy': occupancy_chart_data,
            'staff': staff_chart_data,
            'room_types': room_type_data
        }
        
        return JsonResponse(chart_data)
        
    except Exception as e:
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


def test_view(request):
    """
    Simple test view to diagnose deployment issues
    """
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        # Test static files
        import os
        from django.conf import settings
        static_dir = os.path.join(settings.BASE_DIR, 'static')
        staticfiles_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None
        
        context = {
            'status': 'success',
            'database_connection': 'Working' if result else 'Not working',
            'static_dir_exists': os.path.exists(static_dir),
            'staticfiles_dir': str(staticfiles_dir) if staticfiles_dir else 'Not set',
            'debug_mode': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
        }
    except Exception as e:
        context = {
            'status': 'error',
            'error_message': str(e),
        }
    
    return render(request, 'reports/test_view.html', context)
