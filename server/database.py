import sqlite3

def init_db():
    conn = sqlite3.connect("stats.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_answer(user_id, date, answer):
    conn = sqlite3.connect("stats.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO answers (user_id, date, answer) VALUES (?, ?, ?)",
        (user_id, date, answer)
    )
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect("stats.db")
    c = conn.cursor()
    c.execute("SELECT user_id, date, answer FROM answers ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return data

