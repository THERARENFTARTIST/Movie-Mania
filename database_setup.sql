-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS moviebooking;

-- Use the created database
USE moviebooking;

-- Drop tables if they already exist (useful for resetting)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Create the movies table
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    showtime DATETIME
);

-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    tickets INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Booked',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

-- Insert some sample users
INSERT INTO users (username, password, email) VALUES
('john_doe', 'password123', 'john.doe@example.com'),
('jane_smith', 'securepass456', 'jane.smith@example.com');

-- Insert the sample movies
INSERT INTO movies (name, genre, showtime) VALUES
('Inception', 'Action', '2024-12-20 19:00:00'),
('Avengers: Endgame', 'Action', '2024-12-20 21:30:00'),
('The Dark Knight', 'Action', '2024-12-21 20:00:00'),
('Toy Story 4', 'Adventure', '2024-12-22 18:30:00'),
('The Lord of the Rings', 'Adventure', '2024-12-23 20:30:00'),
('Jurassic Park', 'Adventure', '2024-12-24 19:00:00'),
('The Hangover', 'Comedy', '2024-12-25 20:00:00'),
('Superbad', 'Comedy', '2024-12-26 21:00:00'),
('21 Jump Street', 'Comedy', '2024-12-27 19:30:00');

-- Insert sample bookings
INSERT INTO bookings (user_id, movie_id, booking_date, booking_time, tickets, status) VALUES
(1, 1, '2024-12-20', '19:00:00', 2, 'Booked'),
(2, 3, '2024-12-21', '20:00:00', 1, 'Booked');
