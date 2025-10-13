SELECT DISTINCT h.hotel_id, h.hotel_name
FROM hotel h
JOIN room r ON h.hotel_id = r.hotel_id
ORDER BY h.hotel_name;