import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
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
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings (name, email, date, time, meet_link)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, date, time, meet_link))

    conn.commit()
    conn.close()


def get_all_meetings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meetings")
    meetings = cursor.fetchall()

    conn.close()
    return meetings


def is_slot_available(date, time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM meetings WHERE date=? AND time=?
    """, (date, time))

    result = cursor.fetchone()
    conn.close()

    return result is None


# ✅ NEW FUNCTION (IMPORTANT)
def clear_all_meetings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM meetings")

    conn.commit()
    conn.close()
