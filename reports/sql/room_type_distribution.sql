-- Room Type Distribution
SELECT
    r.room_type,
    COUNT(r.room_id) AS room_count
FROM room r
GROUP BY r.room_type
ORDER BY room_count DESC;