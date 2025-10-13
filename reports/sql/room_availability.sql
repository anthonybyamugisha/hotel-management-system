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