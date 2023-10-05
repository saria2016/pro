-- Prepare the development database on the MySQL server

-- create the development database if it doesn't already exist
 DROP DATABASE IF EXISTS `task_db`;
 CREATE DATABASE IF NOT EXISTS `task_db`;
 USE `task_db`;

-- reduce pasword policy to low
SET GLOBAL validate_password.policy=0;

-- add new user and set a password
CREATE USER IF NOT EXISTS 'task_admin'@'localhost' IDENTIFIED BY 'task_pwd';

-- grant privileges to users on the new database
GRANT ALL PRIVILEGES ON task_db.* TO 'task_admin'@'localhost';

-- grand select privilege to user on performance_schema
GRANT SELECT ON performance_schema.* TO 'task_admin'@'localhost';

FLUSH PRIVILEGES;
