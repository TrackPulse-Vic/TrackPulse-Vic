from utils.search import trainData
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.lines_dictionaries import *

import sqlite3

conn = sqlite3.connect("userdata/trainlogs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    train_id TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")
conn.commit()
user_id = "123456"
train_id = "950M"
timestamp = "2025-05-25 14:30"

cursor.execute(
    "INSERT INTO logs (user_id, train_id, timestamp) VALUES (?, ?, ?)",
    (user_id, train_id, timestamp)
)
conn.commit()
user_id = "123456"
train_id = "950M"
timestamp = "2025-05-25 14:30"

cursor.execute(
    "INSERT INTO logs (user_id, train_id, timestamp) VALUES (?, ?, ?)",
    (user_id, train_id, timestamp)
)
conn.commit()
