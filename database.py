import sqlite3
from datetime import datetime


ADMIN_ID = 70085020 

def is_admin(user_id):
    return user_id == ADMIN_ID


connection = sqlite3.connect("startUp.db")
cursor = connection.cursor()

def create_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number VARCHAR(13) NOT NULL,
        yonalish TEXT NOT NULL,
        StartUp_malumotlari TEXT NOT NULL,
        submission_date DATE NOT NULL DEFAULT (date('now'))
    )
    """)
    connection.commit()

create_database()

def insert_data_database(full_name, phone_number, yonalish, StartUp_malumotlari):
    cursor.execute('''INSERT INTO candidate (full_name, phone_number, yonalish, StartUp_malumotlari) 
                      VALUES (?, ?, ?, ?)''',
                   (full_name, phone_number, yonalish, StartUp_malumotlari))
    connection.commit()

def get_todays_applications():
    today_date = datetime.now().date()
    cursor.execute('''SELECT full_name, phone_number, yonalish, StartUp_malumotlari 
                      FROM candidate 
                      WHERE submission_date = ?''', (today_date,))
    return cursor.fetchall()

def close_connection():
    connection.close()
