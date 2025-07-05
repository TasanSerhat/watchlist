import sqlite3

conn = sqlite3.connect("watchlist.db")
cursor = conn.cursor()

cursor.execute("""Create table if not exists movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    watched INTEGER,
    note TEXT
)
""")

cursor.execute("""Create table if not exists series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    season INTEGER,
    episode INTEGER,
    note TEXT
)
""")

conn.commit()
conn.close()
