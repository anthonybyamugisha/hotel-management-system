-- Hotel Occupancy Rates
SELECT
    h.hotel_name AS Hotel_Name,
    ROUND(
        (SUM(CASE WHEN r.room_status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2
    ) AS Occupancy_Rate
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_name
ORDER BY Occupancy_Rate DESC;