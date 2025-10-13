-- CREATE DATABASE hotel management;
CREATE database hotelmanagementdb;
-- USE hotel management;
USE hotelmanagementdb;

-- Hotel Table
CREATE TABLE hotel (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    Contact VARCHAR(20) NOT NULL
);

CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    staff_role VARCHAR(30) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id)
);

-- Guest Table
CREATE TABLE guest (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL
);

-- Room Table
CREATE TABLE room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    room_type VARCHAR(20),
    room_status VARCHAR(20),
    FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id)
);

-- Booking Table
CREATE TABLE  booking(
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT,
    room_id INT,
    check_in_date DATE,
    check_out_date DATE,
    booking_status VARCHAR(20),
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

-- Payment Table
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    payment_date DATE,
    amount DECIMAL(12,2),
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);

CREATE TABLE invoice (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    guest_id INT,
    reservation_id INT,
    amount DECIMAL(12,2),
    room_status VARCHAR(10),
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id)
);

CREATE TABLE services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    service_price DECIMAL(12,2),
    booking_id INT,
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);

