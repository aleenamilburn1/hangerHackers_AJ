import sqlite3
import random
# import requests

ChallengeCollection = []

challenges = {
    1: "Donate 6 garmets of clothing within 2 weeks",
    2: "Resell 2 garments of clothing within 4 weeks",
    3: "Open the app twice a week for 1 month to keep up with what you own"
}

# randomly select the challenge of the week

def select_random_challenge(challenges, count = 1):
    selected_keys = random.sample(list(challenges.keys()), k = count)
    return {k: challenges[k] for k in selected_keys}


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
    
def update_user_password(email, new_password):
    # Connect to the SQLite database
    conn = sqlite3.connect('closet_manager.db')
    cursor = conn.cursor()
    
    # SQL command to update the password for the user with the given email
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    
    # Commit the changes to the database
    conn.commit()
    
    # Close the connection
    conn.close()

    print("Password updated successfully.")

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

def entryMenu():
    menu2 = input("Select an option: \n 1: Home \n 2: Challenges \n 3: Resell \n 4: Give back \n 5: User profile \n 0: Logout \n")
    if menu2 == '0':
                stop = True
    if menu2 == '1':
                # garments nearing the predetermined deadline
                # insights - usage per type of item over a period of time, expected vs real
                # 
                print("Home \n Current Monthy Usage of Items in Closet \n ")
                entryMenu()
    elif menu2 == '2':
                # different challenge options with the option to opt in or opt out
                
                print("\n Raise your earnings and supplement your savings with some friendly competition! :) \n")
                selected_challenge = select_random_challenge(challenges)
                for key, challenge in selected_challenge.items():
                    print(f"{key}: {challenge} \n")
    elif menu2 == '3':
                print("Financial Summary: \n February Resell Earnings: $33.97 \n Surplus Spending over user's set goal: $18.26 \n")
                entryMenu()
                # earnings summary
                # clothes with similiar garment description and the prices they're sold for
    elif menu2 == '4':
                # takes your location and retrieves closest homeless shelters
                print("There are 8 homeless shelters, women's centers, and/or thrift stores in your area. \n")
                entryMenu()
    elif menu2 == '5':
        menuProf = input("Select an option: \n 1: add to your closet \n 2: view your closet \n 3: view your username and password \n 4: back to main menu \n")
        # add to your closet collection
        if menuProf == '4':
            entryMenu()
        if menuProf == '1':
            userID = input("\nPlease enter your user ID: \n ")
            garmentColor = input("\nPlease enter the garment color: \n")
            garmentType = input("\nPlease input the type of garment: \n")
            garmentOccasion = input("\nPlease input the garment occasion type: \n")
            insert_hanger(
                userID, 
                garmentColor, 
                garmentType, 
                garmentOccasion, 
                1)                    
                
        # view your closet collection
        if menuProf == '2':
            userID = input("\nPlease enter your user ID: \n ")
            get_user_hangers(userID)
                
        # change your password
        if menuProf == '3':
            login()
            if login():
                userID = input("\nPlease enter your user ID: \n ")
                password = input("\nEnter a new password: \n")
                update_user_password()
                        
menu = input("Select an option: \n 1: Register \n 2: Login \n") 

if menu == '0':
        False
elif menu == '1':
    register()
elif menu == '2' :
     if login() == True:
          entryMenu()

stop = False
while not stop:
     entryMenu()



#stop = False
#while not stop:
 #   menu = input("Select an option: \n 1: Register \n 2: Login \n")
 #   if menu == '0':
 #       stop = True
 #   elif menu == '1':
 #       register()
 #   elif menu == '2':
 #       if login() == True:
 #           entryMenu()
  #          
 #   else:
   #     entryMenu()
    #    print("Back to main menu")