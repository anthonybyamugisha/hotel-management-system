-- Report For Guests who have paid the highest amounts

-- Total Amount Paid per Guest
SELECT
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.contact AS guest_contact,
    h.hotel_name,
    SUM(IFNULL(p.amount, 0)) AS total_paid
FROM guest g
JOIN booking b ON g.guest_id = b.guest_id
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id
LEFT JOIN payment p ON b.booking_id = p.booking_id
GROUP BY g.guest_id, g.first_name, g.last_name, h.hotel_name
ORDER BY total_paid DESC
LIMIT 10;  -- Shows top 10 paying guests

-- Total Amount Paid per Guest Across All Hotels
SELECT
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    SUM(IFNULL(p.amount, 0)) AS total_paid
FROM guest g
JOIN booking b ON g.guest_id = b.guest_id
LEFT JOIN payment p ON b.booking_id = p.booking_id
GROUP BY g.guest_id, g.first_name, g.last_name
ORDER BY total_paid DESC
LIMIT 10;
