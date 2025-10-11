from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
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
    # Sample data for demonstration
    # In a real application, you would process the actual data from your SQL queries
    chart_data = {
        'revenue': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'room_revenue': [12000, 19000, 15000, 18000, 22000, 25000],
            'service_revenue': [5000, 7000, 6000, 8000, 9000, 10000]
        },
        'occupancy': {
            'hotels': ['Grand Plaza', 'Seaside Resort', 'City Center Inn', 'Mountain View Hotel'],
            'rates': [75, 82, 68, 79]
        },
        'staff': {
            'departments': ['Reception', 'Housekeeping', 'Food Service', 'Maintenance', 'Management'],
            'scores': [85, 92, 78, 88, 95]
        },
        'room_types': {
            'types': ['Single', 'Double', 'Suite', 'Deluxe', 'Presidential'],
            'counts': [30, 45, 15, 8, 2]
        }
    }
    
    return JsonResponse(chart_data)


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