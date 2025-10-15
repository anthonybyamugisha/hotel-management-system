SELECT
    h.hotel_id,
    h.hotel_name,
    r.room_type,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
    ROUND(
        (SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
    ) AS occupancy_rate_percent
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_id, h.hotel_name, r.room_type
ORDER BY h.hotel_id, r.room_type;