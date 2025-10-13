-- Department Performance Summary
SELECT
    s.staff_role AS department,
    COUNT(DISTINCT b.booking_id) + COUNT(DISTINCT sv.service_id) AS performance_score
FROM staff s
LEFT JOIN room r ON s.hotel_id = r.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
GROUP BY s.staff_role
ORDER BY performance_score DESC;