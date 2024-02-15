import sqlite3
import bcrypt

# checking if the user exists
def user_exists(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# authenticating user password
def authenticate_user(username):
    conn = sqlite3.connect('user_database.db')
    password = input("please enter your password: ")
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    stored_hashed_password = user[4] # user = [id, username, balance, email, password]
    password_attempts = 0

    while not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        print("Authentication failed: Incorrect password")
        password_attempts += 1
        print(f'{3-password_attempts} password attempts left')

        if password_attempts >= 3:
            print("too many attempts")
            quit() # quits the overall program
        password = input("please enter your password: ")


    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        print("Authentication successful")
        return True


# new user creation
def create_user(username, deposit):
    conn = sqlite3.connect('user_database.db')

    print("new user ...")
    email = input("please enter your email: ")
    password = input("please enter a password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn.execute('INSERT INTO users (username, balance, email, password) VALUES (?, ?, ?, ?);', (username, deposit, email, hashed_password))
    print(f"User '{username}' created with an initial balance of '{deposit}.")

    conn.commit()

    # Retrieve the updated user information
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    conn.close()
    return user


# retrieves the user balance
def get_user_balance(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT balance FROM users WHERE username = ?;', (username,))
    user_balance = cursor.fetchone()
    conn.close()

    if user_balance:
        return user_balance[0]  # The balance is the first (and only) element in the tuple
    else:
        return None


def db_main():
    # Create the database and table (if not already created)
    conn = sqlite3.connect('user_database.db')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

    # Create a new user with an initial balance of 0
    username = input("Enter username for the user: ")
    deposit = input("Enter deposit amount: ")

    if not user_exists(username):
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

            return balance, user[1]
    

def update_balance_in_db(username, new_balance):
    conn = sqlite3.connect('user_database.db')
    conn.execute('UPDATE users SET balance = ? WHERE username = ?;', (new_balance, username))
    conn.commit()
    conn.close()


# dev only
def view_users():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users;')
    
    print("User Information:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Username: {row[1]}, balance: {row[2]}, email: {row[3]}, password: {row[4]}")
        # e.g. ID: 1, Username: paul, balance: 110, email: wells@gmail.com, password: b'$2bvLO/2qWwMMPyK'
    conn.close()

if __name__ == "__main__":
    view_users()

