from django import forms
from django.db import connection

class GuestForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
                              widget=forms.Select(attrs={'class': 'form-control'}))

class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Populate guests and rooms dynamically
        with connection.cursor() as cursor:
            cursor.execute("SELECT guest_id, CONCAT(first_name, ' ', last_name) as full_name FROM guest")
            guests = cursor.fetchall()
            self.fields['guest_id'].choices = [('', 'Select Guest')] + [(g[0], g[1]) for g in guests]
            
            cursor.execute("SELECT room_id, CONCAT('Room ', room_id, ' (', room_type, ')') as room_info FROM room WHERE room_status = 'Available'")
            rooms = cursor.fetchall()
            self.fields['room_id'].choices = [('', 'Select Room')] + [(r[0], r[1]) for r in rooms]
    
    guest_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    room_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    booking_status = forms.ChoiceField(
        choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class RoomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        # Populate hotels dynamically
        with connection.cursor() as cursor:
            cursor.execute("SELECT hotel_id, hotel_name FROM hotel")
            hotels = cursor.fetchall()
            self.fields['hotel_id'].choices = [('', 'Select Hotel')] + [(h[0], h[1]) for h in hotels]
    
    hotel_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    room_type = forms.ChoiceField(
        choices=[('Single', 'Single'), ('Double', 'Double'), ('Executive', 'Executive'), ('Ordinary', 'Ordinary')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    room_status = forms.ChoiceField(
        choices=[('Available', 'Available'), ('Occupied', 'Occupied'), ('Booked', 'Booked'), ('Maintenance', 'Maintenance')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class StaffForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        # Populate hotels dynamically
        with connection.cursor() as cursor:
            cursor.execute("SELECT hotel_id, hotel_name FROM hotel")
            hotels = cursor.fetchall()
            self.fields['hotel_id'].choices = [('', 'Select Hotel')] + [(h[0], h[1]) for h in hotels]
    
    hotel_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    staff_role = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PaymentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        # Populate bookings dynamically
        with connection.cursor() as cursor:
            cursor.execute("SELECT booking_id, CONCAT('Booking ', booking_id) as booking_info FROM booking")
            bookings = cursor.fetchall()
            self.fields['booking_id'].choices = [('', 'Select Booking')] + [(b[0], b[1]) for b in bookings]
    
    booking_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    amount = forms.DecimalField(max_digits=12, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))