from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.index, name='reports_index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chart-data/', views.chart_data, name='chart_data'),
    path('general-report/', views.general_report, name='general_report'),
    path('room-occupancy/', views.room_occupancy_report, name='room_occupancy_report'),
    path('staff-performance/', views.staff_performance, name='staff_performance'),
    path('monthly-revenue/', views.monthly_revenue_collection, name='monthly_revenue_collection'),
    path('outstanding-payments/', views.outstanding_payments_per_guest, name='outstanding_payments_per_guest'),
    path('top-paying-guests/', views.top_paying_guests, name='top_paying_guests'),
]