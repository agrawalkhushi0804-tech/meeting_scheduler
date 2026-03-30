import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        date TEXT,
        time TEXT,
        meet_link TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_meeting(name, email, date, time, meet_link):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO meetings (name, email, date, time, meet_link)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email, date, time, meet_link))

    conn.commit()
    conn.close()


def get_all_meetings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meetings")
    data = cursor.fetchall()

    conn.close()
    return data


def is_slot_available(date, time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM meetings WHERE date=? AND time=?
    """, (date, time))

    result = cursor.fetchone()
    conn.close()

    return result is None
