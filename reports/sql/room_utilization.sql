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