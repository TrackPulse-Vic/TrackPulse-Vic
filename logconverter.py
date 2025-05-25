import sqlite3
import csv
import os
import asyncio

async def convertLogsToDB(userid, username):
    with open (f'utils/trainlogger/userdata/{username}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        conn = sqlite3.connect(f'userdata/trainlogs.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            og_id TEXT,
            set_number TEXT,
            train_type TEXT,
            date TEXT,
            line TEXT,
            start TEXT,
            end TEXT,
            notes TEXT,
            username TEXT
            )
        ''')

        for row in reader:
            cursor.execute(f'''
            INSERT INTO logs (user_id, og_id, set_number, train_type, date, line, start, end, notes, username)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (userid, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(username)))

        conn.commit()
        conn.close()
    

if __name__ == "__main__":
    convertLogsToDB('780303451980038165', 'xm9g')