-- Report For Monthly Revenue Collection per Hotel

-- Monthly Revenue from Room Bookings
SELECT
    h.hotel_name,
    DATE_FORMAT(b.check_in_date, '%Y-%m') AS month,
    SUM(i.amount) AS room_revenue
FROM booking b
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id
JOIN invoice i ON b.booking_id = i.booking_id
GROUP BY h.hotel_name, DATE_FORMAT(b.check_in_date, '%Y-%m')
ORDER BY month, h.hotel_name;

-- Monthly Revenue from Services
SELECT
    h.hotel_name,
    DATE_FORMAT(b.check_in_date, '%Y-%m') AS month,
    SUM(sv.service_price) AS service_revenue
FROM services sv
JOIN booking b ON sv.booking_id = b.booking_id
JOIN room r ON b.room_id = r.room_id
JOIN hotel h ON r.hotel_id = h.hotel_id
GROUP BY h.hotel_name, DATE_FORMAT(b.check_in_date, '%Y-%m')
ORDER BY month, h.hotel_name;

-- Combined Monthly Revenue per Hotel
SELECT
    h.hotel_name,
    DATE_FORMAT(b.check_in_date, '%Y-%m') AS month,
    IFNULL(SUM(i.amount), 0) AS room_revenue,
    IFNULL(SUM(sv.service_price), 0) AS service_revenue,
    (IFNULL(SUM(i.amount), 0) + IFNULL(SUM(sv.service_price), 0)) AS total_revenue
FROM hotel h
JOIN room r ON h.hotel_id = r.hotel_id
JOIN booking b ON b.room_id = r.room_id
LEFT JOIN invoice i ON b.booking_id = i.booking_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
GROUP BY h.hotel_name, DATE_FORMAT(b.check_in_date, '%Y-%m')
ORDER BY month, total_revenue DESC;

-- Combined Monthly Revenue per Hotel (Dashboard Version)
SELECT
    DATE_FORMAT(b.check_in_date, '%Y-%m') AS Month,
    IFNULL(SUM(i.amount), 0) AS Total_Room_Revenue,
    IFNULL(SUM(sv.service_price), 0) AS Total_Service_Revenue
FROM hotel h
JOIN room r ON h.hotel_id = r.hotel_id
JOIN booking b ON b.room_id = r.room_id
LEFT JOIN invoice i ON b.booking_id = i.booking_id
LEFT JOIN services sv ON sv.booking_id = b.booking_id
GROUP BY DATE_FORMAT(b.check_in_date, '%Y-%m')
ORDER BY Month;
