import sqlite3


def user_exists(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def create_user(username, deposit):
    conn = sqlite3.connect('user_database.db')
    if not user_exists(username):
        # If the user doesn't exist, insert a new user with the provided deposit
        conn.execute('INSERT INTO users (username, balance) VALUES (?, ?);', (username, deposit))
        print(f"User '{username}' created with an initial balance of '{deposit}.")
    else:
        # If the user exists, update the user's balance by adding the deposit
        conn.execute('UPDATE users SET balance = balance + ? WHERE username = ?;', (deposit, username))
        print(f"Welcome back, {username}! Deposit of '{deposit}' added to your balance.")

    conn.commit()

    # Retrieve the updated user information
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    conn.close()
    return user


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
        balance INTEGER NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

    # Create a new user with an initial balance of 0
    username = input("Enter username for the user: ")
    deposit = input("Enter deposit amount: ")
    user = create_user(username, deposit)
    if user:
        print(f"Username: {user[1]}, with a balance of: {user[2]}")
        balance = get_user_balance(username)
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
        print(f"ID: {row[0]}, Username: {row[1]}, balance: {row[2]}")

    conn.close()

if __name__ == "__main__":
    view_users()

