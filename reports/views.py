from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import os

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


def general_report(request):
    try:
        data = execute_sql('general report.sql')
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