import sqlite3

# --- 1. Database Setup ---
def setup_database():
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
    con.close()

# --- 2. Application Functions ---
def add_new_cruise():
    print("\n--- Add a New Cruise ---")
    cruise_line = input("Cruise Line (e.g., Royal Caribbean): ")
    ship_name = input("Ship Name: ")
    departure_date = input("Departure Date (YYYY-MM-DD): ")
    
    try:
        duration_nights = int(input("Duration in Nights (e.g., 7): "))
    except ValueError:
        print("Error: Duration must be a whole number. Returning to menu.")
        return 

    loyalty_input = input("Loyalty Status (Press Enter to skip): ")
    loyalty_status = loyalty_input if loyalty_input.strip() != "" else None

    try:
        total_fare = float(input("Total Fare (e.g., 950.00): "))
    except ValueError:
        print("Error: Total fare must be a number. Returning to menu.")
        return

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
        print(f"\nFailed to insert data: {error}")
    finally:
        if conn:
            conn.close()

def show_all_cruises():
    print("\n--- All Logged Cruises ---")
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cruises')
    all_cruises = cursor.fetchall()
    
    if not all_cruises:
        print("No cruises logged yet!")
    else:
        for cruise in all_cruises:
            print(f"{cruise[3]} | {cruise[1]} - {cruise[2]} ({cruise[4]} nights)")
    conn.close()

def search_by_line():
    print("\n--- Search Cruises ---")
    search_term = input("Enter a cruise line to search for: ")
    
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    sql = 'SELECT * FROM cruises WHERE cruise_line = ? COLLATE NOCASE'
    cursor.execute(sql, (search_term,))
    results = cursor.fetchall()
    
    if not results:
        print(f"No cruises found for '{search_term}'.")
    else:
        print(f"\nFound {len(results)} cruise(s) for {search_term}:")
        for cruise in results:
            print(f"- {cruise[2]} on {cruise[3]}")
    conn.close()

def sort_cruises_by_date():
    print("\n--- Cruises Sorted by Departure Date ---")
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cruises ORDER BY departure_date DESC')
    sorted_cruises = cursor.fetchall()
    
    if not sorted_cruises:
        print("No cruises to sort!")
    else:
        for cruise in sorted_cruises:
            print(f"{cruise[3]} | {cruise[1]} {cruise[2]}")
    conn.close()

def show_statistics():
    print("\n--- Your Cruise Statistics ---")
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    
    # We use SQL aggregate functions to do the math for us
    cursor.execute('''
        SELECT 
            COUNT(cruise_id), 
            SUM(duration_nights), 
            SUM(total_fare) 
        FROM cruises
    ''')
    
    # fetchone() grabs the single row of results returned by the math functions
    stats = cursor.fetchone() 
    
    # Extract the data from the tuple, defaulting to 0 if the database is empty
    total_cruises = stats[0] or 0
    total_nights = stats[1] or 0
    total_spent = stats[2] or 0.0
    
    if total_cruises == 0:
        print("No cruises logged yet. Add some trips to see your stats!")
    else:
        # Calculate the average cost per night
        cost_per_night = total_spent / total_nights
        
        print(f"Total Cruises: {total_cruises}")
        print(f"Total Nights at Sea: {total_nights}")
        print(f"Total Amount Spent: ${total_spent:.2f}")
        print(f"Average Cost Per Night: ${cost_per_night:.2f}")
        
    conn.close()

def update_cruise():
    print("\n--- Update a Cruise ---")
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    
    # First, list all cruises so the user knows which ID to pick
    cursor.execute('SELECT cruise_id, cruise_line, ship_name, departure_date FROM cruises')
    cruises = cursor.fetchall()
    
    if not cruises:
        print("No cruises available to update!")
        conn.close()
        return
        
    for c in cruises:
        # c[0] is the cruise_id
        print(f"ID {c[0]} | {c[1]} {c[2]} ({c[3]})")
        
    try:
        target_id = int(input("\nEnter the ID of the cruise you want to update: "))
    except ValueError:
        print("Invalid ID format. Returning to menu.")
        conn.close()
        return

    # Fetch the specific record they chose
    cursor.execute('SELECT * FROM cruises WHERE cruise_id = ?', (target_id,))
    record = cursor.fetchone()
    
    if not record:
        print(f"No cruise found with ID {target_id}.")
        conn.close()
        return

    print("\nPress Enter to keep the current value, or type a new one.")
    
    # record indices: 0:id, 1:line, 2:ship, 3:date, 4:nights, 5:loyalty, 6:fare
    new_line = input(f"Cruise Line [{record[1]}]: ") or record[1]
    new_ship = input(f"Ship Name [{record[2]}]: ") or record[2]
    new_date = input(f"Departure Date [{record[3]}]: ") or record[3]
    
    new_nights_input = input(f"Duration in Nights [{record[4]}]: ")
    new_nights = int(new_nights_input) if new_nights_input else record[4]
    
    new_loyalty_input = input(f"Loyalty Status [{record[5] if record[5] else 'None'}]: ")
    # Handle the optional loyalty status
    if new_loyalty_input == "":
        new_loyalty = record[5] # keep existing
    elif new_loyalty_input.lower() == "none":
        new_loyalty = None # allow them to clear it out
    else:
        new_loyalty = new_loyalty_input
        
    new_fare_input = input(f"Total Fare [{record[6]}]: ")
    new_fare = float(new_fare_input) if new_fare_input else record[6]

    # Execute the UPDATE statement
    cursor.execute('''
        UPDATE cruises 
        SET cruise_line = ?, ship_name = ?, departure_date = ?, duration_nights = ?, loyalty_status = ?, total_fare = ?
        WHERE cruise_id = ?
    ''', (new_line, new_ship, new_date, new_nights, new_loyalty, new_fare, target_id))
    
    conn.commit()
    print("\nSuccess! Cruise updated.")
    conn.close()

def delete_cruise():
    print("\n--- Delete a Cruise ---")
    conn = sqlite3.connect('cruise_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT cruise_id, cruise_line, ship_name, departure_date FROM cruises')
    cruises = cursor.fetchall()
    
    if not cruises:
        print("No cruises available to delete!")
        conn.close()
        return
        
    for c in cruises:
        print(f"ID {c[0]} | {c[1]} {c[2]} ({c[3]})")
        
    try:
        target_id = int(input("\nEnter the ID of the cruise you want to delete: "))
    except ValueError:
        print("Invalid ID format. Returning to menu.")
        conn.close()
        return

    # Fetch it first so we can name the ship in the confirmation prompt
    cursor.execute('SELECT cruise_line, ship_name FROM cruises WHERE cruise_id = ?', (target_id,))
    record = cursor.fetchone()
    
    if not record:
        print(f"No cruise found with ID {target_id}.")
        conn.close()
        return

    # The confirmation safeguard
    confirm = input(f"\nAre you SURE you want to delete your trip on the {record[0]} {record[1]}? (y/n): ")
    
    if confirm.lower() == 'y':
        cursor.execute('DELETE FROM cruises WHERE cruise_id = ?', (target_id,))
        conn.commit()
        print("\nRecord permanently deleted.")
    else:
        print("\nPhew! Deletion cancelled. Your record is safe.")
        
    conn.close()

# --- 3. The Main Menu Loop ---
def main():
    # Make sure the table exists before we do anything else
    setup_database()
    
    while True:
        print("\n" + "="*25)
        print("   CRUISE TRACKER MENU")
        print("="*25)
        print("1. Add a New Cruise")
        print("2. Show All Cruises")
        print("3. Search by Cruise Line")
        print("4. Sort by Departure Date")
        print("5. Show Statistics")
        print("6. Update a Cruise")
        print("7. Delete a Cruise")
        print("8. Quit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == '1':
            add_new_cruise()
        elif choice == '2':
            show_all_cruises()
        elif choice == '3':
            search_by_line()
        elif choice == '4':
            sort_cruises_by_date()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            update_cruise()
        elif choice == '7':
            delete_cruise()
        elif choice == '8':
            print("\nClosing Cruise Tracker. Bon voyage!\n")
            break # This exits the while loop and ends the program
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")

# This tells Python to run the main() function when you start the file
if __name__ == "__main__":
    main()