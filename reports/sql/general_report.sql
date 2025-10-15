-- Comprehensive Hotel Summary
SELECT
    h.hotel_id,
    h.hotel_name,
    h.location,
    h.Contact AS hotel_contact,

    -- Staff summary
    COUNT(DISTINCT s.staff_id) AS total_staff,

    -- Room summary by type
    SUM(CASE WHEN r.room_type = 'Single' THEN 1 ELSE 0 END) AS total_single_rooms,
    SUM(CASE WHEN r.room_type = 'Double' THEN 1 ELSE 0 END) AS total_double_rooms,
    SUM(CASE WHEN r.room_type = 'Executive' THEN 1 ELSE 0 END) AS total_executive_rooms,
    SUM(CASE WHEN r.room_type = 'Ordinary' THEN 1 ELSE 0 END) AS total_ordinary_rooms,
    COUNT(r.room_id) AS total_rooms_overall,

    -- Financial summary
    SUM(IFNULL(i.amount,0)) AS total_invoiced,
    SUM(IFNULL(p.amount,0)) AS total_paid,
    SUM(IFNULL(i.amount,0) - IFNULL(p.amount,0)) AS total_outstanding,
    
    -- Services revenue
    SUM(IFNULL(sv.service_price,0)) AS total_service_revenue

FROM hotel h
LEFT JOIN staff s ON h.hotel_id = s.hotel_id
LEFT JOIN room r ON h.hotel_id = r.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
LEFT JOIN invoice i ON i.booking_id = b.booking_id
LEFT JOIN payment p ON p.booking_id = b.booking_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id

GROUP BY h.hotel_id, h.hotel_name, h.location, h.Contact
ORDER BY h.hotel_name;
