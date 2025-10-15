-- Report: Staff Performance and Workload per Hotel

-- Staff List with Assigned Hotel
SELECT
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
    s.staff_role,
    s.contact AS staff_contact,
    h.hotel_name
FROM staff s
JOIN hotel h ON s.hotel_id = h.hotel_id
ORDER BY h.hotel_name, s.staff_role, s.staff_id;

-- Staff Workload: Number of Bookings per Hotel
SELECT
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
    s.staff_role,
    h.hotel_name,
    COUNT(b.booking_id) AS total_bookings_handled
FROM staff s
JOIN hotel h ON s.hotel_id = h.hotel_id
LEFT JOIN room r ON r.hotel_id = h.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
WHERE s.staff_role IN ('Manager', 'Receptionist')
GROUP BY s.staff_id, s.staff_role, h.hotel_name
ORDER BY total_bookings_handled DESC, s.staff_name;

-- Staff Contribution to Services
SELECT
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
    s.staff_role,
    h.hotel_name,
    COUNT(sv.service_id) AS total_services_handled
FROM staff s
JOIN hotel h ON s.hotel_id = h.hotel_id
LEFT JOIN room r ON r.hotel_id = h.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
WHERE s.staff_role IN ('Chef', 'Cleaner', 'Waiter', 'Housekeeper')
GROUP BY s.staff_id, s.staff_role, h.hotel_name
ORDER BY total_services_handled DESC, s.staff_name;

-- Combined Staff Performance Summary
SELECT
    s.staff_id,
    s.first_name,
    s.last_name,
    h.hotel_name,
    s.staff_role,
    s.contact,
    (COUNT(DISTINCT b.booking_id) + COUNT(DISTINCT sv.service_id)) AS performance_score
FROM staff s
JOIN hotel h ON s.hotel_id = h.hotel_id
LEFT JOIN room r ON r.hotel_id = h.hotel_id
LEFT JOIN booking b ON b.room_id = r.room_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
GROUP BY s.staff_id, s.first_name, s.last_name, h.hotel_name, s.staff_role, s.contact
ORDER BY performance_score DESC, s.staff_role, s.first_name, s.last_name;
