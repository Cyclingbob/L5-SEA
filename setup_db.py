import sqlite3
from config import database_file

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

enable_foreign_keys_q = "PRAGMA foreign_keys = ON;"
cursor.execute(enable_foreign_keys_q)

create_user_q = '''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    admin BOOLEAN NOT NULL DEFAULT 0
);
'''

cursor.execute(create_user_q)

create_project_q = '''
CREATE TABLE IF NOT EXISTS Projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    owner INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner)
        REFERENCES Users (id)
        ON DELETE CASCADE
);
'''

cursor.execute(create_project_q)

create_user_project_q = '''
CREATE TABLE IF NOT EXISTS UserProjects (
    user_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    role TEXT NOT NULL,

    PRIMARY KEY (user_id, project_id),

    FOREIGN KEY (user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (project_id)
        REFERENCES Projects(id)
        ON DELETE CASCADE
);
'''

cursor.execute(create_user_project_q)

create_system_q = '''
CREATE TABLE IF NOT EXISTS Systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    project_id INTEGER NOT NULL,
    FOREIGN KEY (project_id)
        REFERENCES Projects(id)
        ON DELETE CASCADE
);
'''

cursor.execute(create_system_q)

create_component_q = '''
CREATE TABLE IF NOT EXISTS Components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    part_number TEXT NOT NULL UNIQUE,
    unit_cost REAL NOT NULL
);
'''

cursor.execute(create_component_q)

create_system_component_q = '''
CREATE TABLE IF NOT EXISTS SystemComponents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id INTEGER NOT NULL,
    system_id INTEGER NOT NULL,

    FOREIGN KEY (component_id)
        REFERENCES Components(id)
        ON DELETE CASCADE,
    
    FOREIGN KEY (system_id)
        REFERENCES Systems(id)
        ON DELETE CASCADE
)
'''

cursor.execute(create_system_component_q)

create_connection_q = '''
CREATE TABLE IF NOT EXISTS Connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_component_a INTEGER NOT NULL,
    system_component_b INTEGER NOT NULL,
    component_a_label TEXT NOT NULL,
    component_b_label TEXT NOT NULL,
        
    FOREIGN KEY (system_component_a)
        REFERENCES SystemComponents(id)
        ON DELETE CASCADE,
    
    FOREIGN KEY (system_component_b)
        REFERENCES SystemComponents(id)
        ON DELETE CASCADE
);
'''

cursor.execute(create_connection_q)
connection.commit()
connection.close()
print("Setup database!")