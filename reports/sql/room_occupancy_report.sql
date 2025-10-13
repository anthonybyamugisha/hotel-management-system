-- Report For Room Occupancy and Utilization per Hotel

-- Room Status per Hotel
SELECT 
    h.hotel_id,
    h.hotel_name,
    r.room_type,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.room_status = 'Available' THEN 1 ELSE 0 END) AS available_rooms,
    SUM(CASE WHEN r.room_status = 'Booked' THEN 1 ELSE 0 END) AS booked_rooms,
    SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
    SUM(CASE WHEN r.room_status = 'Maintenance' THEN 1 ELSE 0 END) AS maintenance_rooms
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_id, r.room_type
ORDER BY h.hotel_id, r.room_type;

-- Detailed Room Status with Guest Bookings
SELECT
    h.hotel_name,
    r.room_id,
    r.room_type,
    r.room_status,
    b.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    b.check_in_date,
    b.check_out_date,
    b.booking_status
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
LEFT JOIN booking b ON r.room_id = b.room_id
LEFT JOIN guest g ON b.guest_id = g.guest_id
ORDER BY h.hotel_name, r.room_type, r.room_id;

-- Hotel Occupancy Rate
SELECT
    h.hotel_name,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
    ROUND(
        (SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
    ) AS occupancy_rate_percent
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_name
ORDER BY occupancy_rate_percent DESC;