# Run setup_db.py first!

import unittest
import hashlib
import sqlite3
import os
import subprocess

from database import Database, hashPassword
from config import database_file

if os.path.exists(database_file): # Wipe old database
    os.remove(database_file)

subprocess.run(["python", "setup_db.py"], check=True) # Setup a new one

db = Database(database_file)
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

class TestDBMethods(unittest.TestCase):
    def test_1_create(self):
        first_name = "John"
        surname = "Doe"
        email = "john.doe@test.com"
        password = "SecretPassword"
        hashedPassword = hashPassword(password)

        result = db.createUser(first_name, surname, email, password)
        self.assertEqual(result, "success")

        select_user_q = '''
            SELECT first_name, surname, email, password FROM Users WHERE email = ?
        '''

        cursor.execute(select_user_q, (email, )) # extra comma needed for tuple
        connection.commit()
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1) # Email should be unique
        
        returned_row = rows[0]
        returned_first_name = returned_row[0]
        returned_surname = returned_row[1]
        returned_email = returned_row[2]
        returned_hashed_password = returned_row[3]

        self.assertEqual(returned_first_name, first_name)
        self.assertEqual(returned_surname, surname)
        self.assertEqual(returned_email, email)
        self.assertEqual(returned_hashed_password, hashedPassword)

    def test_2_edit(self):
        email = "john.doe@test.com"

        select_user_q = '''
            SELECT id FROM Users WHERE email = ?
        '''

        cursor.execute(select_user_q, (email,))
        rows = cursor.fetchall()

        self.assertTrue(len(rows) > 0, "User not found for edit")

        id = rows[0][0]

        new_first = "Jane"
        new_surname = "Smith"
        new_email = "jane.smith@test.com"
        new_password = "NewPassword"
        new_hashed_password = hashPassword(new_password)

        result = db.editUser(id, new_first, new_surname, new_email, new_hashed_password)

        self.assertEqual(result, "success", result)

        verify_q = '''
            SELECT first_name, surname, email, password FROM Users WHERE id = ?
        '''

        cursor.execute(verify_q, (id,))
        updated_rows = cursor.fetchall()

        self.assertEqual(len(updated_rows), 1)

        row = updated_rows[0]

        self.assertEqual(row[0], new_first)
        self.assertEqual(row[1], new_surname)
        self.assertEqual(row[2], new_email)

    def test_3_login(self):
        email = "jane.smith@test.com"
        password = "NewPassword"

        result = db.login(email, password)

        # Result format: "ID:PasswordHash"
        self.assertTrue(":" in result, "Login failed: " + result)

        returned_id = result.split(":")[0]

        select_user_q = '''
            SELECT id FROM Users WHERE email = ?
        '''

        cursor.execute(select_user_q, (email,))
        rows = cursor.fetchall()

        self.assertTrue(len(rows) == 1)

        expected_id = str(rows[0][0])

        self.assertEqual(returned_id, expected_id)

    def test_4_delete(self):
        select_user_q = '''
            SELECT id FROM Users WHERE email = ?
        '''

        email = "jane.smith@test.com"

        cursor.execute(select_user_q, (email, ))
        connection.commit()
        rows = cursor.fetchall()
        
        self.assertTrue(len(rows) > 0, "Nothing to delete")

        id = rows[0][0]

        result = db.deleteUser(id)
        self.assertEqual(result, "success", result) # Error message

        new_select_user_q = '''
            SELECT id FROM Users WHERE id = ?
        '''

        cursor.execute(new_select_user_q, (id, ))
        connection.commit()
        new_rows = cursor.fetchall()

        self.assertTrue(len(new_rows) == 0, "Item wasn't deleted")

if __name__ == '__main__':
    unittest.main()