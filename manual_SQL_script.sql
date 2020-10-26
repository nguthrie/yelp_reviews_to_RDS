SHOW DATABASES;
DROP DATABASE yelp_reivews;
CREATE DATABASE yelp_scaper_project;
USE yelp_scaper_project;
CREATE TABLE review_data (username VARCHAR(20) PRIMARY KEY, 
review_date DATE, star_rating INT, friend_count INT, 
review_text VARCHAR(500));
DROP TABLE review_data;
SHOW TABLES;

SHOW VARIABLES LIKE 'local_infile';



LOAD DATA LOCAL INFILE 'C:/Users/Nicholas/Programming/webscraper/reviews.csv'
INTO TABLE review_data;

FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

