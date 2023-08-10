-- Creates a table users following these requirements:
-- The table has these attributes:
--    id, integer, never null, auto increment and primary key
--    email, string (255 characters), never null and unique
--    name, string (255 characters)
--    If the table already exists, this script does not fail
--    This script can be executed on any database

CREATE TABLE users IF NOT EXISTS (
    id  AUTO_INCREMENT INT PRIMARY KEY,
    email  VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
