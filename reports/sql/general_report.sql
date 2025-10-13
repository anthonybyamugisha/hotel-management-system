-- General Report for Hotel Management Database

-- Hotels and Staff
SELECT 
    h.hotel_id,
    h.hotel_name,
    h.location,
    h.Contact AS hotel_contact,
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
    s.staff_role,
    s.contact AS staff_contact
FROM hotel h
LEFT JOIN staff s ON h.hotel_id = s.hotel_id
ORDER BY h.hotel_id, s.staff_id;

-- Guests and Their Bookings
SELECT 
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.contact AS guest_contact,
    g.gender,
    b.booking_id,
    b.room_id,
    r.room_type,
    r.room_status,
    b.check_in_date,
    b.check_out_date,
    b.booking_status
FROM guest g
LEFT JOIN booking b ON g.guest_id = b.guest_id
LEFT JOIN room r ON b.room_id = r.room_id
ORDER BY g.guest_id, b.booking_id;

-- Room Status Summary per Hotel
SELECT
    h.hotel_id,
    h.hotel_name,
    r.room_type,
    r.room_status,
    COUNT(*) AS total_rooms
FROM hotel h
LEFT JOIN room r ON h.hotel_id = r.hotel_id
GROUP BY h.hotel_id, h.hotel_name, r.room_type, r.room_status
ORDER BY h.hotel_name, r.room_type, r.room_status;

-- Payments per Booking
SELECT 
    p.payment_id,
    p.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    p.payment_date,
    p.amount
FROM payment p
JOIN booking b ON p.booking_id = b.booking_id
JOIN guest g ON b.guest_id = g.guest_id
ORDER BY p.payment_id;

-- Invoices with Outstanding Balances
SELECT
    i.invoice_id,
    i.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    i.amount AS total_invoice_amount,
    IFNULL(SUM(p.amount), 0) AS total_paid,
    (i.amount - IFNULL(SUM(p.amount),0)) AS outstanding_balance,
    i.room_status
FROM invoice i
JOIN booking b ON i.booking_id = b.booking_id
JOIN guest g ON b.guest_id = g.guest_id
LEFT JOIN payment p ON p.booking_id = b.booking_id
GROUP BY i.invoice_id, i.booking_id, g.guest_id, i.amount, i.room_status
ORDER BY outstanding_balance DESC;

-- Services Used by Guests
SELECT
    sv.service_id,
    sv.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    sv.service_name,
    sv.service_price
FROM services sv
JOIN booking b ON sv.booking_id = b.booking_id
JOIN guest g ON b.guest_id = g.guest_id
ORDER BY sv.service_id;

-- Total Payments per Guest
SELECT
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    SUM(IFNULL(p.amount,0)) AS total_paid,
    SUM(i.amount - IFNULL(p.amount,0)) AS total_outstanding
FROM guest g
LEFT JOIN booking b ON g.guest_id = b.guest_id
LEFT JOIN invoice i ON b.booking_id = i.booking_id
LEFT JOIN payment p ON b.booking_id = p.booking_id
GROUP BY g.guest_id
ORDER BY total_paid DESC;

-- Summary: Services Revenue per Type
SELECT
    sv.service_name,
    COUNT(*) AS service_count,
    SUM(sv.service_price) AS total_revenue
FROM services sv
GROUP BY sv.service_name
ORDER BY total_revenue DESC;

-- Booking Status Summary
SELECT
    b.booking_status,
    COUNT(*) AS total_bookings
FROM booking b
GROUP BY b.booking_status
ORDER BY total_bookings DESC;

-- Hotel Revenue Summary
SELECT
    h.hotel_id,
    h.hotel_name,
    SUM(i.amount) AS total_invoiced,
    SUM(IFNULL(p.amount,0)) AS total_paid,
    SUM(i.amount - IFNULL(p.amount,0)) AS total_outstanding,
    SUM(IFNULL(sv.service_price,0)) AS total_service_revenue
FROM hotel h
LEFT JOIN room r ON h.hotel_id = r.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
LEFT JOIN invoice i ON i.booking_id = b.booking_id
LEFT JOIN payment p ON p.booking_id = b.booking_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
GROUP BY h.hotel_id, h.hotel_name
ORDER BY total_invoiced DESC;
