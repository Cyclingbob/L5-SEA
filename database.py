import sqlite3
import hashlib

def hashPassword(password) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class Database:
    def __init__(self, file):
        self.file = file
        self._connection = sqlite3.connect(file, check_same_thread=False)
        self._cursor = self._connection.cursor()

    def createUser(self, first_name, surname, email, password):
        insert_user_q = """
            INSERT INTO Users (first_name, surname, email, password)
            VALUES (?, ?, ?, ?)
        """

        hashedPassword = hashPassword(password)

        try:
            self._cursor.execute(insert_user_q, (
                first_name,
                surname,
                email,
                hashedPassword
            ))
            self._connection.commit()
            return self._cursor.lastrowid # ID of the new item
        except sqlite3.Error as e:
            print(f"Create user failed {first_name} {surname}: ", e)
            return str(e)
        
    def deleteUser(self, id):
        delete_user_q = '''
            DELETE FROM Users WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_user_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete user failed with id: {id}: " + str(e))
            return str(e)
    
    def editUser(self, id, first_name, surname, email, password):
        update_user_q = '''
            UPDATE Users
            SET first_name = ?, surname = ?, email = ?, password = ?
            WHERE id = ?
        '''

        try:
            self._cursor.execute(update_user_q, (first_name, surname, email, password, id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit user failed with id: {id} " + str(e))
            return str(e)
        
    def login(self, email, password):
        select_user_q = '''
            SELECT id, password FROM Users WHERE email = ?
        '''

        try:
            self._cursor.execute(select_user_q, (email,))
            self._connection.commit()
            rows = self._cursor.fetchall()

            # Array of (id, password)
            if len(rows) > 0:
                stored_password = rows[0][1]
                hashed_password = hashPassword(password)
                if stored_password == hashed_password:
                    return str(rows[0][0]) + ":" + rows[0][1] # "ID:Password"
                else:
                    return "wrongpassword"
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Edit failed with id: {id} " + str(e))
            return "Failed:" + str(e)
        
    def getUser(self, id):
        select_user_q = '''
            SELECT first_name, surname, email, password, admin, id FROM Users WHERE id = ?
        '''

        try:
            self._cursor.execute(select_user_q, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()

            # Array of (first_name, surname, email, password)
            
            if isinstance(rows, list):
                if len(rows) > 0:
                    return {
                        "first_name": rows[0][0],
                        "surname": rows[0][1],
                        "email": rows[0][2],
                        "password": rows[0][3],
                        "isAdmin": rows[0][4] == 1,
                        "id": rows[0][5]
                    }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"GetUser failed with id: {id} " + str(e))
            return str(e)
        
    def userExists(self, email):
        select_user_q = '''
            SELECT EXISTS(SELECT 1 FROM Users WHERE email = ? LIMIT 1)
        '''

        try:
            self._cursor.execute(select_user_q, (email, ))
            self._connection.commit()
            exists = self._cursor.fetchone()[0]

            return exists == 1
        except sqlite3.Error as e:
            print(f"UserExists failed with email: {email} " + str(e))
            return str(e)

    def getAllUsers(self):
        select_users_q = '''
            SELECT first_name, surname, email, admin, id FROM Users
        '''

        try:
            self._cursor.execute(select_users_q)
            self._connection.commit()
            rows = self._cursor.fetchall()
            
            users = []
            if len(rows) > 0:
                for row in rows:
                    users.append({
                        "first_name": row[0],
                        "surname": row[1],
                        "email": row[2],
                        "isAdmin": row[3] == 1,
                        "id": row[4]
                    })
                return users
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetAllUsers failed: " + str(e))
            return str(e)

    def createProject(self, name, category, description, owner):
        insert_project_q = """
            INSERT INTO Projects (name, category, description, owner)
            VALUES (?, ?, ?, ?)
        """

        try:
            self._cursor.execute(insert_project_q, (
                name,
                category,
                description,
                owner
            ))
            self._connection.commit()
            return self._cursor.lastrowid # ID of the new item
        except sqlite3.IntegrityError as e:
            print(f"Create Project Integrity Error Duplicate Item " + str(e))
            return "duplicate"
        except sqlite3.Error as e:
            print(f"Create project failed {name}: ", e)
            return "Failed: " + str(e)
    
    def deleteProject(self, id):
        delete_proj_q = '''
            DELETE FROM Projects WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_proj_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete project failed with id: {id}: " + str(e))
            return str(e)
        
    def editProject(self, id, name, category, description):
        update_project_q = '''
            UPDATE Projects
            SET name = ?, category = ?, description = ?
            WHERE id = ?
        '''

        try:
            self._cursor.execute(update_project_q, (name, category, description, id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit project failed with id: {id} " + str(e))
            return str(e)
      
    def getAllProjects(self):
        select_project_q = '''
            SELECT name, category, description, id, owner FROM Projects
        '''

        try:
            self._cursor.execute(select_project_q)
            self._connection.commit()
            rows = self._cursor.fetchall()

            projects = []
            for row in rows:
                projects.append({
                    "name": row[0],
                    "category": row[1],
                    "description": row[2],
                    "id": row[3],
                    "owner": row[4]
                })
            return projects
        except sqlite3.Error as e:
            print(f"GetAllProjects failed" + str(e))
            return str(e)
    
    def getProject(self, id):
        select_project_id = '''
            SELECT name, category, description, created_at, id, owner FROM Projects
            WHERE id = ?
        '''

        try:
            self._cursor.execute(select_project_id, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                return {
                    "name": rows[0][0],
                    "category": rows[0][1],
                    "description": rows[0][2],
                    "created_at": rows[0][3],
                    "id": rows[0][4],
                    "owner": rows[0][5]
                }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetProject failed with id: {id} " + str(e))
            return str(e)
    
    def createUserProject(self, user_id, project_id, role):
        insert_project_q = """
            INSERT INTO UserProjects (user_id, project_id, role)
            VALUES (?, ?, ?)
        """

        try:
            self._cursor.execute(insert_project_q, (
                user_id,
                project_id,
                role
            ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Create UserProject failed: user {user_id}, project {project_id}: ", e)
            return str(e)

    def getUserProjects(self, user_id):
        select_user_projects_q = '''
            SELECT Projects.name, Projects.category, Projects.description, UserProjects.role, UserProjects.project_id FROM Projects
            JOIN UserProjects ON Projects.id = UserProjects.project_id
            WHERE UserProjects.user_id = ?
        '''

        try:
            self._cursor.execute(select_user_projects_q, (user_id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                user_projects = []
                for row in rows:
                    user_projects.append({
                        "name": row[0],
                        "category": row[1],
                        "description": row[2],
                        "role": row[3],
                        "project_id": row[4]
                    })
                return user_projects
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetUserProjects failed with id: {id} " + str(e))
            return str(e)
    
    def getProjectUsers(self, project_id):
        select_project_users_q = '''
            SELECT Users.first_name, Users.surname, Users.email, Users.admin, UserProjects.role, UserProjects.user_id FROM Users
            JOIN UserProjects ON Users.id = UserProjects.user_id
            WHERE UserProjects.project_id = ?
        '''

        try:
            self._cursor.execute(select_project_users_q, (project_id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            
            project_users = []
            if len(rows) > 0:
                for row in rows:
                    project_users.append({
                        "first_name": row[0],
                        "surname": row[1],
                        "email": row[2],
                        "isAdmin": row[3] == 1,
                        "role": row[4],
                        "user_id": row[5]
                    })
                return project_users
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetProjecUsers failed with project_id: {project_id} " + str(e))
            return str(e)
    
    def editUserProject(self, user_id, project_id, role):
        update_user_project_q = '''
            UPDATE UserProjects
            SET project_id = ?, role = ?
            WHERE user_id = ?
        '''

        try:
            self._cursor.execute(update_user_project_q, (project_id, role, user_id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit UserProject failed with user {user_id}, project {project_id}: " + str(e))
            return str(e)

    def deleteUserProject(self, user_id, project_id):
        delete_user_proj_q = '''
            DELETE FROM UserProjects WHERE user_id = ? and project_id = ?
        '''

        try:
            self._cursor.execute(delete_user_proj_q, (user_id, project_id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit DeleteUserProject failed with user {user_id}, project {project_id}: " + str(e))
            return str(e)

    def createSystem(self, name, category, description, project_id):
        insert_system_q = """
            INSERT INTO Systems (name, category, description, project_id)
            VALUES (?, ?, ?, ?)
        """

        try:
            self._cursor.execute(insert_system_q, (
                name,
                category,
                description,
                project_id
            ))
            self._connection.commit()
            return self._cursor.lastrowid # ID of system created
        except sqlite3.Error as e:
            print(f"Create system failed {name} : ", e)
            return str(e)

    def deleteSystem(self, id):
        delete_system_q = '''
            DELETE FROM Systems WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_system_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete system failed with id: {id}: " + str(e))
            return str(e)

    def editSystem(self, system_id, name, category, description, project_id):
        update_system_q = '''
            UPDATE Systems
            SET project_id = ?, name = ?, category = ?, description = ?
            WHERE id = ?
        '''

        try:
            self._cursor.execute(update_system_q, (project_id, name, category, description, system_id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit System failed with system {name} ({system_id}), project {project_id}: " + str(e))
            return str(e)

    def getSystem(self, id):
        select_system_id = '''
            SELECT name, category, description, project_id, created_at FROM Systems
            WHERE id = ?
        '''

        try:
            self._cursor.execute(select_system_id, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                return {
                    "name": rows[0][0],
                    "category": rows[0][1],
                    "description": rows[0][2],
                    "project_id": rows[0][3],
                    "created_at": rows[0][4]
                }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetSystem failed with id: {id} " + str(e))
            return str(e)

    def getProjectSystems(self, id):
        select_project_id = '''
            SELECT id, name, category, description, created_at FROM Systems
            WHERE project_id = ?
        '''

        try:
            self._cursor.execute(select_project_id, (id, ))
            # self._connection.commit()
            rows = self._cursor.fetchall()

            if len(rows) == 0:
                return "notfound"

            systems = []
            for row in rows:
                systems.append({
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "description": row[3],
                    "created_at": row[4]
                })

            return systems
        except sqlite3.Error as e:
            print(f"Failed: GetProjectSystems failed with id: {id} " + str(e))
            return str(e)

    def createComponent(self, name, type, part_number, unit_cost):
        insert_system_q = """
            INSERT INTO Components (name, type, part_number, unit_cost)
            VALUES (?, ?, ?, ?)
        """

        try:
            self._cursor.execute(insert_system_q, (
                name,
                type,
                part_number,
                unit_cost
            ))
            self._connection.commit()

            return self._cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Create component failed {name} : ", e)
            return str(e)

    def editComponent(self, id, name, type, part_number, unit_cost):
        update_user_project_q = '''
            UPDATE Components
            SET name = ?, type = ?, part_number = ?, unit_cost = ?
            WHERE id = ?
        '''

        try:
            self._cursor.execute(update_user_project_q, (name, type, part_number, unit_cost, id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit Component failed with system {name} ({id}): " + str(e))
            return str(e)

    def deleteComponent(self, id):
        delete_component_q = '''
            DELETE FROM Components WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_component_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete Component failed with id: {id}: " + str(e))
            return str(e)

    def getComponent(self, id):
        select_system_id = '''
            SELECT name, type, part_number, unit_cost created FROM Components
            WHERE id = ?
        '''

        try:
            self._cursor.execute(select_system_id, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                return {
                    "name": rows[0][0],
                    "type": rows[0][1],
                    "part_number": rows[0][2],
                    "unit_cost": rows[0][3]
                }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetComponent failed with id: {id} " + str(e))
            return str(e)

    def getAllComponents(self):
        select_all_components_q = '''
            SELECT name, type, part_number, unit_cost, id FROM Components
        '''

        try:
            self._cursor.execute(select_all_components_q)
            self._connection.commit()
            rows = self._cursor.fetchall()

            projects = []
            for row in rows:
                projects.append({
                    "name": row[0],
                    "type": row[1],
                    "part_number": row[2],
                    "unit_cost": row[3],
                    "id": row[4]
                })
            return projects
        except sqlite3.Error as e:
            print(f"GetAllComponents failed: " + str(e))
            return str(e)
   
    def createSystemComponent(self, system_id, component_id):
        insert_system_component_q = """
            INSERT INTO SystemComponents (system_id, component_id)
            VALUES (?, ?)
        """

        try:
            self._cursor.execute(insert_system_component_q, (
                system_id,
                component_id
            ))
            self._connection.commit()

            return self._cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Failed: Create system component failed system: {system_id}, component_id: {component_id} : ", e)
            return str(e)

    def deleteSystemComponent(self, id):
        delete_system_component_q = '''
            DELETE FROM SystemComponents WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_system_component_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete SystemComponent failed with id: {id}: " + str(e))
            return str(e)

    def getSystemComponent(self, id):
        select_system_component_id = '''
            SELECT component_id, system_id created FROM SystemComponents
            WHERE id = ?
        '''

        try:
            self._cursor.execute(select_system_component_id, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                return {
                    "component_id": rows[0][0],
                    "system_id": rows[0][1]
                }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetSystemComponent failed with id: {id} " + str(e))
            return str(e)

    def getAllSystemComponents(self, system_id):
        select_all_system_components_q = '''
            SELECT id, component_id FROM SystemComponents
            WHERE system_id = ?
        '''

        try:
            self._cursor.execute(select_all_system_components_q, (system_id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()

            projects = []
            for row in rows:
                projects.append({
                    "id": row[0],
                    "component_id": row[1]
                })
            return projects
        except sqlite3.Error as e:
            print(f"GetAllComponents failed: " + str(e))
            return str(e)
   
    def getComponentUsed(self, component_id):  # Check if there are any components in use before deleting a component
        select_all_system_components_q = '''
            SELECT id, system_id FROM SystemComponents
            WHERE component_id = ?
        '''

        try:
            self._cursor.execute(select_all_system_components_q, (component_id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()

            systems = []
            for row in rows:
                systems.append({
                    "id": row[0],
                    "system_id": row[1]
                })
            return systems
        except sqlite3.Error as e:
            print(f"getComponentsUsed failed: " + str(e))
            return str(e)

    def createConnection(self, systemComponentA, systemComponentB, componentALabel, componentBLabel):
        insert_connection_q = """
            INSERT INTO Connections (system_component_a, system_component_b, component_a_label, component_b_label)
            VALUES (?, ?, ?, ?)
        """

        try:
            self._cursor.execute(insert_connection_q, (
                systemComponentA,
                systemComponentB,
                componentALabel,
                componentBLabel
            ))
            self._connection.commit()
            return self._cursor.lastrowid # ID of the new item
        except sqlite3.Error as e:
            print(f"Create Connection failed A: {systemComponentA}. B: ${systemComponentB} : ", e)
            return str(e)

    def deleteConnection(self, id):
        delete_connection_q = '''
            DELETE FROM Connections WHERE id = ?
        '''

        try:
            self._cursor.execute(delete_connection_q, (id, ))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Delete connection failed with id: {id}: " + str(e))
            return str(e)

    def editConnection(self, component_a, component_b, component_a_label, component_b_label, id):
        update_user_project_q = '''
            UPDATE Connections
            SET component_a = ?, component_b = ?, component_a_label = ?, component_b_label
            WHERE id = ?
        '''

        try:
            self._cursor.execute(update_user_project_q, (component_a, component_b, component_a_label, component_b_label, id))
            self._connection.commit()
            return "success"
        except sqlite3.Error as e:
            print(f"Edit Connection failed with {id}: " + str(e))
            return str(e)

    def getConnection(self, id):
        select_connection_id = '''
            SELECT system_component_a, system_component_b, component_a_label, component_b_label created FROM Connections
            WHERE id = ?
        '''

        try:
            self._cursor.execute(select_connection_id, (id, ))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                return {
                    "component_a": rows[0][0],
                    "component_b": rows[0][1],
                    "component_a_label": rows[0][2],
                    "component_b_label": rows[0][3]
                }
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetConnection failed with id: {id} " + str(e))
            return str(e)

    def getSystemConnections(self, system_id):
        select_system_connections_q = '''
            SELECT c.system_component_a, c.system_component_b, c.component_a_label, c.component_b_label, c.id FROM Connections c
            JOIN SystemComponents ca ON ca.id = c.system_component_a
            JOIN SystemComponents cb ON cb.id = c.system_component_a
            WHERE ca.system_id = ?
            AND cb.system_id = ?
        '''

        try:
            self._cursor.execute(select_system_connections_q, (system_id, system_id))
            self._connection.commit()
            rows = self._cursor.fetchall()
            if len(rows) > 0:
                system_components = []
                for row in rows:
                    system_components.append({
                        "component_a": row[0],
                        "component_b": row[1],
                        "component_a_label": row[2],
                        "component_b_label": row[3],
                        "id": row[4]
                    })
                return system_components
            else:
                return "notfound"
        except sqlite3.Error as e:
            print(f"Failed: GetSystemConnections failed with id: {system_id} " + str(e))
            return str(e)