import sqlite3

# 1. First, we set up the database and table (Runs every time, safely)
con = sqlite3.connect('cruise_tracker.db')
cur = con.cursor()

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
con.close() # Close this initial setup connection!

# 2. Define our function to add data
def add_new_cruise():
    print("\n--- Add a New Cruise ---")
    
    cruise_line = input("Cruise Line (e.g., Royal Caribbean): ")
    ship_name = input("Ship Name: ")
    departure_date = input("Departure Date (YYYY-MM-DD): ")
    
    try:
        duration_nights = int(input("Duration in Nights (e.g., 7): "))
    except ValueError:
        print("Error: Duration must be a whole number. Please try again.")
        return 

    loyalty_input = input("Loyalty Status (Press Enter to skip): ")
    loyalty_status = loyalty_input if loyalty_input.strip() != "" else None

    try:
        total_fare = float(input("Total Fare (e.g., 950.00): "))
    except ValueError:
        print("Error: Total fare must be a number. Please try again.")
        return

    # Open a fresh connection just for inserting the data
    try:
        conn = sqlite3.connect('cruise_tracker.db')
        cursor = conn.cursor()
        
        sql = '''
        INSERT INTO cruises 
        (cruise_line, ship_name, departure_date, duration_nights, loyalty_status, total_fare)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (cruise_line, ship_name, departure_date, duration_nights, loyalty_status, total_fare))
        conn.commit()
        print(f"\nSuccess! Your trip on the {ship_name} has been saved.")
        
    except sqlite3.Error as error:
        print(f"\nFailed to insert data into sqlite table: {error}")
        
    finally:
        if conn:
            conn.close() # Safely close the function's connection

# 3. Actually run the function
add_new_cruise()