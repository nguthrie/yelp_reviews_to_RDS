import pymysql
import credentials

db = pymysql.connect(credentials.database, credentials.user,
                     credentials.password, local_infile=True)
cursor = db.cursor()


def show_databases():
    sql = '''show databases;'''
    cursor.execute(sql)
    for databases in cursor:
        print(databases[0])


def create_project_database():
    sql = '''CREATE DATABASE yelp_scaper_project;'''
    cursor.execute(sql)


def use_database():
    sql = '''USE yelp_scaper_project;'''
    cursor.execute(sql)


def create_review_table():
    sql = '''CREATE TABLE review_data (username VARCHAR(20) PRIMARY KEY, 
    review_date VARCHAR(10), star_rating INT, friend_count INT, 
    review_count INT, review_text TEXT);'''
    cursor.execute(sql)


def show_tables():
    sql = '''SHOW TABLES;'''
    cursor.execute(sql)
    for table in cursor:
        print(table[0])


def select_all_data_in_table():
    sql = '''SELECT *
    FROM review_data;'''
    cursor.execute(sql)
    for row in cursor:
        print(row)


def drop_table():
    sql = '''DROP TABLE review_data;'''
    cursor.execute(sql)


def check_inline_status():
    sql = '''SHOW VARIABLES LIKE 'local_infile';'''
    cursor.execute(sql)
    for result in cursor:
        print(result)


def load_local_data():
    sql = '''LOAD DATA LOCAL INFILE 'C:/Users/Nicholas/Programming/webscraper/reviews.csv'
    INTO TABLE review_data FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;'''
    cursor.execute(sql)


if __name__ == "__main__":

    use_database()
    drop_table()
    create_review_table()
    load_local_data()
    select_all_data_in_table()
