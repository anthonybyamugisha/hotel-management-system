SELECT 
    r.room_id,
    r.room_type,
    r.room_status,
    h.hotel_name,
    h.hotel_id
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
ORDER BY h.hotel_name, r.room_id;