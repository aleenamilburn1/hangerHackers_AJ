import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    
    # Create 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create 'hangers' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hangers (
            hanger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            garment_color TEXT,
            garment_type TEXT,
            garment_occasion TEXT,
            weight_state TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Create 'weight_data' table for storing time-series data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weight_data (
            data_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hanger_id INTEGER,
            timestamp DATETIME,
            weight_state TEXT,
            FOREIGN KEY (hanger_id) REFERENCES hangers (hanger_id)
        )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

create_database()

def insert_user(email, password):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

def insert_hanger(user_id, garment_color, garment_type, garment_occasion, weight_state):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO hangers (user_id, garment_color, garment_type, garment_occasion, weight_state) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, garment_color, garment_type, garment_occasion, weight_state))
    conn.commit()
    conn.close()

def update_weight(hanger_id, new_weight_state):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weight_data (hanger_id, timestamp, weight_state) VALUES (?, datetime('now'), ?)", 
                   (hanger_id, new_weight_state))
    conn.commit()
    conn.close()

def get_user_hangers(user_id):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hangers WHERE user_id=?", (user_id,))
    hangers = cursor.fetchall()
    conn.close()
    return hangers

def get_hanger_weight_data(hanger_id):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weight_data WHERE hanger_id=? ORDER BY timestamp DESC", (hanger_id,))
    weight_data = cursor.fetchall()
    conn.close()
    return weight_data

def verify_user_login(email, input_password):
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    
    # Query to find a user with the matching email and password
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, input_password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return True  # User found, login successful
    else:
        return False  # No match found, login failed


# Register for an account
def register():
    username = input("Please enter your email as a username \n")
    password = input("Please enter a password \n")
    insert_user(username,password)
    
    


# Login using an account that has already been registered

def login():
    username = input("Please enter your username \n")
    password = input("Please enter your password \n")
    login_successful = verify_user_login(username,password)

    if login_successful:
        print("Login successful!")
        return True
    else:
        print("Login failed. Please check your email and password.")
        return False


stop = False
while stop is False:
    menu = input("Select an option: \n 1: Register \n 2: Login \n")
    if menu == '0':
        break
    if menu == '1':
        register()
    elif menu == '2':
        if login():
            menu2 = input("Select an option: \n 1: Home \n 2: ")
