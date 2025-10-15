# SQL Files Documentation

This document describes the purpose and implementation of each SQL file in the reports/sql directory.

## Report SQL Files

### general_report.sql
**Purpose**: Provides a comprehensive overview of hotel operations
**Data Included**:
- Hotel information (ID, name, location, contact)
- Staff summary (total staff count)
- Room inventory by type (Single, Double, Executive, Ordinary)
- Financial summary (total invoiced, paid, outstanding)
- Service revenue summary
**Used In**: General Report page

### room_occupancy_report.sql
**Purpose**: Shows detailed room occupancy information by hotel and room type
**Data Included**:
- Hotel ID and name
- Room type
- Total rooms count
- Occupied rooms count
- Occupancy rate percentage
**Used In**: Room Occupancy Report page

### staff_performance.sql
**Purpose**: Evaluates staff performance based on bookings and services handled
**Data Included**:
- Staff ID, name, role, and contact
- Hotel name
- Number of bookings handled
- Number of services handled
- Total activity score
**Used In**: Staff Performance Report page

### monthly_revenue_collection.sql
**Purpose**: Tracks monthly revenue from room bookings and services
**Data Included**:
- Month (YYYY-MM format)
- Total room revenue
- Total service revenue
- Combined total revenue
**Used In**: Monthly Revenue Collection Report page and Dashboard charts

### outstanding_payments_per_guest.sql
**Purpose**: Identifies guests with outstanding payment balances
**Data Included**:
- Guest ID and name
- Total amount paid
- Total outstanding balance
**Used In**: Outstanding Payments Per Guest Report page

### top_paying_guests.sql
**Purpose**: Ranks guests by total amount paid
**Data Included**:
- Guest ID and name
- Total amount paid
**Used In**: Top Paying Guests Report page

### hotel_occupancy_rates.sql
**Purpose**: Calculates occupancy rates for each hotel
**Data Included**:
- Hotel name
- Occupancy rate percentage
**Used In**: Dashboard - Hotel Occupancy Rates chart

### room_type_distribution.sql
**Purpose**: Shows the distribution of room types across all hotels
**Data Included**:
- Room type
- Count of rooms
**Used In**: Dashboard - Room Type Distribution chart

### department_performance.sql
**Purpose**: Measures performance scores by staff department/role
**Data Included**:
- Department/Role name
- Performance score
**Used In**: Dashboard - Staff Performance chart

### hotels_and_staff.sql
**Purpose**: Lists hotels with their associated staff members
**Data Included**:
- Hotel information
- Staff information for each hotel
**Used In**: Hotels and Staff Report page

## Essential Project Files

### database_and_table_creation.sql
**Purpose**: Creates the database schema and tables
**Data Included**:
- Database creation statement
- Table definitions for hotel, staff, guest, room, booking, payment, invoice, and services
**Usage**: Database setup and initialization

### populating_tables.sql
**Purpose**: Populates the database with sample data
**Data Included**:
- Sample data for all tables
- Realistic hotel management scenario data
**Usage**: Database population for testing and demonstration

## Template SQL Files

### room_management.sql
**Purpose**: Contains SQL queries used in the room management views
**Data Included**:
- Queries for room listings, availability, status details, and utilization
**Usage**: Room Management page backend queries