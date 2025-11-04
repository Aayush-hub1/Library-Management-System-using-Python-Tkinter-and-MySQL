-- Create Database
CREATE DATABASE IF NOT EXISTS LIBRARY;
USE LIBRARY;

-- Create Books Table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(50),
    price FLOAT,
    quantity INT
);

-- Insert Sample Data
INSERT INTO books (title, author, genre, price, quantity) VALUES
('The Alchemist', 'Paulo Coelho', 'Fiction', 350.00, 10),
('Python Programming', 'John Zelle', 'Education', 550.00, 5),
('Deep Work', 'Cal Newport', 'Self-Help', 450.00, 8),
('Atomic Habits', 'James Clear', 'Self-Help', 400.00, 12),
('Harry Potter', 'J.K. Rowling', 'Fantasy', 600.00, 15);

-- Show All Books
SELECT * FROM books;

-- Find all Self-Help books
SELECT * FROM books WHERE genre = 'Self-Help';

-- Update quantity for a book
UPDATE books SET quantity = 20 WHERE title = 'Atomic Habits';

-- Delete a book entry by ID
DELETE FROM books WHERE book_id = 3;

-- Display final state of table
SELECT * FROM books;
