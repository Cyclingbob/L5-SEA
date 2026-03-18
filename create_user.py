import sqlite3
import argparse
import hashlib
from config import database_file
# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

parser = argparse.ArgumentParser(description="Create a user")

parser.add_argument('first_name', type=str)
parser.add_argument('surname', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--admin', action='store_true', help='Make the user an admin')

insert_user_q = """
INSERT INTO Users (first_name, surname, email, password, admin)
VALUES (?, ?, ?, ?, ?)
"""

args = parser.parse_args()

password_hash = hashlib.sha256(args.password.encode()).hexdigest()

cursor.execute(insert_user_q, (
    args.first_name,
    args.surname,
    args.email,
    password_hash,
    1 if args.admin else 0
))

try:
    connection.commit()
    cursor.execute("SELECT first_name, surname, email, admin FROM Users WHERE rowid = ?", (cursor.lastrowid,))
    print("Successfully created user.")
except sqlite3.Error as e:
    print(f"Failed to create user because of database error: ", e)
    
connection.close()