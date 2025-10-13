-- Hotels and Staff Report
SELECT 
    h.hotel_id,
    h.hotel_name,
    h.location,
    h.Contact AS hotel_contact,
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
    s.staff_role,
    s.contact AS staff_contact
FROM hotel h
LEFT JOIN staff s ON h.hotel_id = s.hotel_id
ORDER BY h.hotel_id, s.staff_id;