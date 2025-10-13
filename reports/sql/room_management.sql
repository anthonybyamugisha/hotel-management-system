-- Room Management Queries

-- Get all rooms with hotel information
SELECT 
    r.room_id,
    r.room_number,
    r.room_type,
    r.room_status,
    r.floor_number,
    r.nightly_rate,
    h.hotel_name,
    h.location
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
ORDER BY h.hotel_name, r.room_number;

-- Get room availability by hotel
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
ORDER BY h.hotel_name, r.room_type;

-- Get detailed room status with current guest information
SELECT 
    h.hotel_name,
    r.room_id,
    r.room_number,
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
ORDER BY h.hotel_name, r.room_number;

-- Get rooms by status
SELECT 
    r.room_id,
    r.room_number,
    r.room_type,
    r.room_status,
    h.hotel_name,
    h.location
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
WHERE r.room_status = %s  -- Parameter for status filter
ORDER BY h.hotel_name, r.room_number;

-- Get room utilization rate by hotel
SELECT
    h.hotel_name,
    COUNT(r.room_id) AS total_rooms,
    ROUND(
        (SUM(CASE WHEN r.room_status IN ('Occupied', 'Booked') THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
    ) AS utilization_rate_percent
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_name
ORDER BY utilization_rate_percent DESC;