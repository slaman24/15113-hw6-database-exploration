import sqlite3

# Connect to (or create) a database file
con = sqlite3.connect('cruise_tracker.db')
cur = con.cursor()

# Create your table (if it doesn't already exist)
cur.execute('''
    CREATE TABLE IF NOT EXISTS cruises (
        cruise_id INTEGER PRIMARY KEY,
        cruise_line TEXT NOT NULL,
        ship_name TEXT NOT NULL,
        departure_date TEXT NOT NULL,
        duration_nights INTEGER NOT NULL,
        loyalty_status TEXT,
        total_fare REAL NOT NULL
    )
''')
con.commit()