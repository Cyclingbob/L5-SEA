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
        self.assertEqual(result, 1) # ID of firsy item

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

# Project tests

class TestProjectMethods(unittest.TestCase):
    def test_5_create_project(self):
        # First create a user (owner)
        user_id = db.createUser("Helen", "Owner", "Helen@test.com", "Password123")

        name = "Project Alpha"
        category = "Software"
        description = "Test project"
        owner = user_id

        result = db.createProject(name, category, description, owner)
        self.assertEqual(result, 1)

        query = '''
            SELECT name, category, description, owner FROM Projects WHERE name = ?
        '''
        cursor.execute(query, (name,))
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)

        row = rows[0]
        self.assertEqual(row[0], name)
        self.assertEqual(row[1], category)
        self.assertEqual(row[2], description)
        self.assertEqual(row[3], owner)

    def test_6_edit_project(self):
        # Get project ID
        query = "SELECT id FROM Projects WHERE name = ?"
        cursor.execute(query, ("Project Alpha",))
        rows = cursor.fetchall()

        self.assertTrue(len(rows) > 0, "Project not found for edit")

        project_id = rows[0][0]

        new_name = "Project Beta"
        new_category = "Hardware"
        new_description = "Updated project"

        result = db.editProject(project_id, new_name, new_category, new_description)
        self.assertEqual(result, "success", result)

        verify_q = '''
            SELECT name, category, description FROM Projects WHERE id = ?
        '''
        cursor.execute(verify_q, (project_id,))
        updated_rows = cursor.fetchall()

        self.assertEqual(len(updated_rows), 1)

        row = updated_rows[0]
        self.assertEqual(row[0], new_name)
        self.assertEqual(row[1], new_category)
        self.assertEqual(row[2], new_description)

    def test_7_delete_project(self):
        query = "SELECT id FROM Projects WHERE name = ?"
        cursor.execute(query, ("Project Beta",))
        rows = cursor.fetchall()

        self.assertTrue(len(rows) > 0, "Nothing to delete")

        project_id = rows[0][0]

        result = db.deleteProject(project_id)
        self.assertEqual(result, "success", result)

        verify_q = "SELECT id FROM Projects WHERE id = ?"
        cursor.execute(verify_q, (project_id,))
        new_rows = cursor.fetchall()

        self.assertEqual(len(new_rows), 0, "Project wasn't deleted")

    def test_8_project_duplicate_name(self):
        user_id = db.createUser("Bob", "Test", "bob@test.com", "Password123")

        db.createProject("UniqueProj", "Test", "Desc", user_id)
        result = db.createProject("UniqueProj", "Test", "Desc", user_id)

        self.assertNotEqual(result, 1)  #should fail

    def test_9_project_invalid_owner(self):
        result = db.createProject("BadProj", "Test", "Desc", 9999)
        self.assertNotEqual(result, 1)

# Test user projects

class TestUserProjectMethods(unittest.TestCase):
    def test_10_create_user_project(self):
        user_id = db.createUser("Tom", "Link", "tom@test.com", "Password123")
        project_id = db.createProject("Link Project", "Test", "Desc", user_id)

        role = "Developer"

        result = db.createUserProject(user_id, project_id, role)

        self.assertTrue(isinstance(result, str))
        self.assertEqual(result, "success")

        query = '''
            SELECT user_id, project_id, role FROM UserProjects
            WHERE user_id = ? AND project_id = ?
        '''
        cursor.execute(query, (user_id, project_id))
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)

        row = rows[0]
        self.assertEqual(row[0], user_id)
        self.assertEqual(row[1], project_id)
        self.assertEqual(row[2], role)

    def test_11_duplicate_user_project(self):
        user_id = db.createUser("Dup", "User", "dup@test.com", "Password123")
        project_id = db.createProject("Dup Project", "Test", "Desc", user_id)

        db.createUserProject(user_id, project_id, "Tester")
        result = db.createUserProject(user_id, project_id, "Tester")

        self.assertTrue(isinstance(result, str))
        self.assertNotEqual(result, "success")

    def test_12_update_user_role(self):
        user_id = db.createUser("Role", "User", "role@test.com", "Password123")
        project_id = db.createProject("Role Project", "Test", "Desc", user_id)

        db.createUserProject(user_id, project_id, "Viewer")

        new_role = "Admin"

        result = db.editUserProject(user_id, project_id, new_role)
        self.assertEqual(result, "success", result)

        query = '''
            SELECT role FROM UserProjects
            WHERE user_id = ? AND project_id = ?
        '''
        cursor.execute(query, (user_id, project_id))
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], new_role)

    def test_13_delete_user_project(self):
        user_id = db.createUser("Del", "User", "del@test.com", "Password123")
        project_id = db.createProject("Del Project", "Test", "Desc", user_id)

        db.createUserProject(user_id, project_id, "Dev")

        result = db.deleteUserProject(user_id, project_id)
        self.assertEqual(result, "success", result)

        query = '''
            SELECT * FROM UserProjects
            WHERE user_id = ? AND project_id = ?
        '''
        cursor.execute(query, (user_id, project_id))
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 0, "UserProject wasn't deleted")

if __name__ == '__main__':
    unittest.main()