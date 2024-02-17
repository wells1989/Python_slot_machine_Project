import sqlite3
import bcrypt
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

## USER LOGIC

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

    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    conn.close()
    return user


def user_exists(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


## USER BALANCE LOGIC

def get_user_balance(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT balance FROM users WHERE username = ?;', (username,))
    user_balance = cursor.fetchone()
    conn.close()

    if user_balance:
        return user_balance[0]  # The balance is the first (and only) element in the tuple
    else:
        return None
    

def update_balance_in_db(username, new_balance):
    conn = sqlite3.connect('user_database.db')
    conn.execute('UPDATE users SET balance = ? WHERE username = ?;', (new_balance, username))
    conn.commit()
    conn.close()


## AUTHENTICATION LOGIC

# switches the user from blocked to unblocked to stop them from logging in / allow them to log in
def switch__user_block(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * from users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    if user[5] == 1:
        conn.execute('UPDATE users SET User_Blocked = ? WHERE username = ?;', (0, username,))
    elif user[5] == 0:
        conn.execute('UPDATE users SET User_Blocked = ? WHERE username = ?;', (1, username,))

    conn.commit()
    conn.close()


# returns true if user is blocked i.e. User_Blocked value is True / 1
def is_user_blocked(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * from users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    conn.close()

    return user[5] == 1


# authenticating user password
def authenticate_user(username):
    conn = sqlite3.connect('user_database.db')

    if is_user_blocked(username):
        print("Your account has been blocked due to multiple failed password attempts, please get in touch to unblock it")
        send_password_reset_email(username)
        quit()

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
            send_email(user[3], "Account Security Alert", "<h2 style="">Important Message</h2><br><p>Too many password attempts for our site. If it was you please contact us to confirm your identity</p>")
            switch__user_block(username)
            quit() # quits the overall program
        password = input("please enter your password: ")


    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        print("Authentication successful")
        return True


def send_email(user_email, subject,body):
    smtp_server = os.environ.get("smtp_server")
    smtp_port = os.environ.get("smtp_port")
    sender_email = os.environ.get("sender_email")
    sender_password = os.environ.get("sender_password")

    # creating the message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    # setting up connection to SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())
    

# password_reset_email .... NOTE: Dummy reset_link for dev only
def send_password_reset_email(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    conn.close()

    reset_link = f"http://your_app_domain/reset_password?username={user[1]}"
    send_email(user[3], "Password Reset", f"<h2>Resetting your password</h2><br><p>You have requested to change your password, via the below link. If you did not request this contact us immediately</p></br><a href={reset_link}>Click here</a>")
    

# changing password based on above (dev only as would need a domain name for the request)
def change_password(username):
    new_password = input("enter new password: ")
    new_password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * from users WHERE username = ?;', (username,))
    user = cursor.fetchone()

    if user[5] == 1:
        switch__user_block(username)

    conn.execute('UPDATE USERS SET password = ? WHERE username = ?;', (new_password_hashed, username,))
    print("password changed successfully")
    conn.commit()


## DEV ONLY (viewing users)
def view_users():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.execute('SELECT * FROM users;')
    
    print("User Information:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Username: {row[1]}, balance: {row[2]}, email: {row[3]}, password: {row[4]}, User_Blocked: {row[5]}")
        # e.g. ID: 1, Username: paul, balance: 110, email: wells@gmail.com, password: b'$2bvLO/2qWwMMPyK'
    conn.close()

if __name__ == "__main__":
    view_users()