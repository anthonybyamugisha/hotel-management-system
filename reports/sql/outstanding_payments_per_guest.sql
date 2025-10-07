-- Outstanding Payments Per Guest Based on Invoices and Payments

-- Detailed Outstanding Balances Per Guest
SELECT
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.contact AS guest_contact,
    h.hotel_name,
    b.booking_id,
    i.amount AS total_invoice_amount,
    IFNULL(SUM(p.amount), 0) AS total_paid,
    (i.amount - IFNULL(SUM(p.amount), 0)) AS outstanding_balance
FROM guest g
JOIN booking b ON g.guest_id = b.guest_id
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id
JOIN invoice i ON b.booking_id = i.booking_id
LEFT JOIN payment p ON b.booking_id = p.booking_id
GROUP BY g.guest_id, b.booking_id, i.amount, h.hotel_name
HAVING outstanding_balance > 0
ORDER BY outstanding_balance DESC;

-- Total Outstanding Amount per Hotel
SELECT
    h.hotel_name,
    SUM(i.amount - IFNULL(paid.total_paid, 0)) AS total_outstanding
FROM invoice i
JOIN booking b ON i.booking_id = b.booking_id
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id
LEFT JOIN (
    SELECT booking_id, SUM(amount) AS total_paid
    FROM payment
    GROUP BY booking_id
) AS paid ON i.booking_id = paid.booking_id
WHERE (i.amount - IFNULL(paid.total_paid, 0)) > 0
GROUP BY h.hotel_name
ORDER BY total_outstanding DESC;

-- Total Outstanding Amount per Guest
SELECT
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    SUM(i.amount - IFNULL(paid.total_paid, 0)) AS total_outstanding_balance
FROM guest g
JOIN booking b ON g.guest_id = b.guest_id
JOIN invoice i ON b.booking_id = i.booking_id
LEFT JOIN (
    SELECT booking_id, SUM(amount) AS total_paid
    FROM payment
    GROUP BY booking_id
) AS paid ON i.booking_id = paid.booking_id
WHERE (i.amount - IFNULL(paid.total_paid, 0)) > 0
GROUP BY g.guest_id
ORDER BY total_outstanding_balance DESC;
