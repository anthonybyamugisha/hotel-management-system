SELECT 
    h.hotel_name,
    r.room_id,
    r.room_type,
    r.room_status,
    b.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    b.check_in_date,
    b.check_out_date
FROM room r
JOIN hotel h ON r.hotel_id = h.hotel_id
LEFT JOIN booking b ON r.room_id = b.room_id AND b.booking_status = 'Confirmed'
LEFT JOIN guest g ON b.guest_id = g.guest_id
ORDER BY h.hotel_name, r.room_id;