import sqlite3
from db.db_utils.db_utils import user_exists, authenticate_user, change_password, create_user, get_user_balance, update_balance_in_db


def db_main():
    # Create the database and table (if not already created)
    conn = sqlite3.connect('user_database.db')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        User_Blocked BOOLEAN DEFAULT FALSE
    );
    ''')
    conn.commit()
    conn.close()


    # Create a new user with an initial balance of 0
    username = input("Enter username for the user: ")

    if not user_exists(username):
        deposit = input("Enter deposit amount: ")
        user = create_user(username, deposit)
        print(f"Username: {user[1]}, with a balance of: {user[2]}")
        balance = get_user_balance(username)
        return balance, user[1]
    
    else:
        print("existing user...")
        if authenticate_user(username):
            balance = get_user_balance(username)
            conn = sqlite3.connect('user_database.db')
            
            cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
            user = cursor.fetchone()
            conn.close()

            password_change_option = input("If you want to change your password click c: ")
            if password_change_option == "c":
                change_password(username)

            return balance, user[1]
    

