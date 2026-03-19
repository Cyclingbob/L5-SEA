import sqlite3
from config import database_file

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

from database import hashPassword

users = [
    {
        "first_name": "Jane",
        "surname": "Doe",
        "email": "jane.doe@example.com",
        "password": "password123"
    },
    {
        "first_name": "Joe",
        "surname": "Smith",
        "email": "joe.smith@example.com",
        "password": "password123"
    },
    {
        "first_name": "John",
        "surname": "Smith",
        "email": "john.smith@example.com",
        "password": "password123"
    },
    {
        "first_name": "Emily",
        "surname": "Johnson",
        "email": "emily.johnson@example.com",
        "password": "password123"
    },
    {
        "first_name": "Michael",
        "surname": "Brown",
        "email": "michael.brown@example.com",
        "password": "password123"
    },
    {
        "first_name": "Sarah",
        "surname": "Davis",
        "email": "sarah.davis@example.com",
        "password": "password123"
    },
    {
        "first_name": "David",
        "surname": "Wilson",
        "email": "david.wilson@example.com",
        "password": "password123"
    },
    {
        "first_name": "Laura",
        "surname": "Taylor",
        "email": "laura.taylor@example.com",
        "password": "password123"
    },
    {
        "first_name": "Chris",
        "surname": "Anderson",
        "email": "chris.anderson@example.com",
        "password": "password123"
    },
    {
        "first_name": "Emma",
        "surname": "Thomas",
        "email": "emma.thomas@example.com",
        "password": "password123"
    }
]

for user in users:
    user["password"] = hashPassword(user["password"])

insert_users_q = """
    INSERT INTO Users (first_name, surname, email, password)
    VALUES (?, ?, ?, ?)
"""

users_tuple = [
    (user["first_name"], user["surname"], user["email"], user["password"])
    for user in users
]

cursor.executemany(insert_users_q, users_tuple)
connection.commit()

select_users_q = """
    SELECT first_name, surname, email, password, id
    FROM Users
"""

cursor.execute(select_users_q)
rows = cursor.fetchall()
print(rows)

projects = [
    {
        "name": "FalconEye Radar Upgrade",
        "category": "Radar Systems",
        "description": "Upgrade of airborne radar processing algorithms to improve target detection and tracking in contested environments.",
        "owner": 3
    },
    {
        "name": "SkyShield Electronic Warfare Suite",
        "category": "Electronic Warfare",
        "description": "Development of a next-generation electronic warfare system for threat detection, jamming, and countermeasure deployment.",
        "owner": 7
    },
    {
        "name": "Aquila UAV Control System",
        "category": "Autonomous Systems",
        "description": "Design of a scalable control architecture for unmanned aerial vehicles with autonomous navigation capabilities.",
        "owner": 1
    },
    {
        "name": "Helios Avionics Integration",
        "category": "Avionics",
        "description": "Integration of flight control, navigation, and communication subsystems into a unified avionics platform.",
        "owner": 5
    },
    {
        "name": "StormWatch ISR Platform",
        "category": "Surveillance",
        "description": "Development of an intelligence, surveillance, and reconnaissance platform for real-time battlefield awareness.",
        "owner": 9
    },
    {
        "name": "Viper Missile Guidance Software",
        "category": "Defence Systems",
        "description": "Implementation of precision guidance algorithms for improved targeting accuracy in missile systems.",
        "owner": 2
    },
    {
        "name": "Orion Sensor Fusion Engine",
        "category": "Data Processing",
        "description": "Creation of a sensor fusion engine combining radar, infrared, and electronic signals for enhanced situational awareness.",
        "owner": 6
    },
    {
        "name": "Titan Ground Radar Network",
        "category": "Radar Systems",
        "description": "Deployment of a distributed ground-based radar network for wide-area airspace monitoring and threat detection.",
        "owner": 4
    },
    {
        "name": "Nova Secure Communications",
        "category": "Communications",
        "description": "Development of encrypted communication protocols for secure data exchange across defence platforms.",
        "owner": 8
    },
    {
        "name": "EagleEye Target Tracking System",
        "category": "Tracking Systems",
        "description": "Advanced tracking system using AI techniques to improve identification and tracking of fast-moving targets.",
        "owner": 10
    }
]

insert_projects_q = """
    INSERT INTO Projects (name, category, description, owner)
    VALUES (?, ?, ?, ?)
"""

projecs_tuple = [
    (project["name"], project["category"], project["description"], project["owner"])
    for project in projects
]

cursor.executemany(insert_projects_q, projecs_tuple)
connection.commit()

select_projects_q = """
    SELECT name, category, description, owner, id
    FROM Projects
"""

cursor.execute(select_projects_q)
rows = cursor.fetchall()
print(rows)

user_projects = [
    {"user_id": 2, "project_id": 1, "role": "Systems Engineer"},              # owner is 3
    {"user_id": 3, "project_id": 2, "role": "Radar Engineer"},                # owner is 7
    {"user_id": 4, "project_id": 3, "role": "Integration Engineer"},          # owner is 1
    {"user_id": 1, "project_id": 4, "role": "Software Engineer"},             # owner is 5
    {"user_id": 6, "project_id": 5, "role": "Data Engineer"},                 # owner is 9
    {"user_id": 5, "project_id": 6, "role": "Avionics Engineer"},             # owner is 2
    {"user_id": 7, "project_id": 7, "role": "Electronic Warfare Specialist"}, # owner is 6
    {"user_id": 8, "project_id": 8, "role": "Communications Engineer"},       # owner is 4
    {"user_id": 10, "project_id": 9, "role": "AI/ML Engineer"},               # owner is 8
    {"user_id": 9, "project_id": 10, "role": "Systems Integration Engineer"}, # owner is 10
]

insert_user_projects_q = """
    INSERT INTO UserProjects (user_id, project_id, role)
    VALUES (?, ?, ?)
"""

user_projecs_tuple = [
    (user["user_id"], user["project_id"], user["role"])
    for user in user_projects
]

cursor.executemany(insert_user_projects_q, user_projecs_tuple)
connection.commit()

select_user_projects_q = """
    SELECT user_id, project_id, role
    FROM UserProjects
"""

cursor.execute(select_user_projects_q)
rows = cursor.fetchall()
print(rows)

systems = [
    # Project 1 - FalconEye Radar Upgrade
    {
        "name": "Radar Signal Processor Unit",
        "category": "Processing Hardware",
        "description": "High-speed signal processing unit connected to the radar antenna array via RF front-end modules. Interfaces with mission computer over Ethernet for real-time data processing.",
        "project_id": 1
    },
    {
        "name": "Antenna Control Interface",
        "category": "Control System",
        "description": "Controls radar antenna positioning motors via PWM drivers. Connected to the main processor over CAN bus for precise beam steering commands.",
        "project_id": 1
    },

    # Project 2 - SkyShield Electronic Warfare Suite
    {
        "name": "Threat Detection Receiver",
        "category": "RF System",
        "description": "Wideband RF receiver connected to multiple antenna inputs. Feeds digitised signals into the EW processor via high-speed serial interface.",
        "project_id": 2
    },
    {
        "name": "Jamming Transmission Module",
        "category": "Transmission System",
        "description": "High-power transmission module connected to directional antennas. Receives jamming instructions from the control unit over a secure Ethernet link.",
        "project_id": 2
    },

    # Project 3 - Aquila UAV Control System
    {
        "name": "Flight Control Computer",
        "category": "Embedded System",
        "description": "Central flight controller connected to IMU, GPS, and actuator systems via UART and I2C. Outputs control signals to servos and ESCs.",
        "project_id": 3
    },
    {
        "name": "Telemetry Communication Module",
        "category": "Communications",
        "description": "Handles bidirectional data link between UAV and ground station. Connected to onboard computer via UART and external antenna via RF connector.",
        "project_id": 3
    },

    # Project 4 - Helios Avionics Integration
    {
        "name": "Mission Computer",
        "category": "Computing",
        "description": "Core avionics processor interfacing with all subsystems over ARINC 429 and Ethernet. Handles navigation, flight data, and pilot display outputs.",
        "project_id": 4
    },
    {
        "name": "Navigation Sensor Suite",
        "category": "Sensors",
        "description": "Includes GPS, INS, and air data sensors. Connected to the mission computer via serial interfaces for continuous position and velocity updates.",
        "project_id": 4
    },

    # Project 5 - StormWatch ISR Platform
    {
        "name": "Electro-Optical Camera System",
        "category": "Imaging",
        "description": "High-resolution EO camera mounted on a gimbal. Connected to processing unit via HDMI/SDI for live video feed.",
        "project_id": 5
    },
    {
        "name": "Data Processing Unit",
        "category": "Processing",
        "description": "Processes ISR data streams and compresses video for transmission. Interfaces with storage and communication modules via Ethernet.",
        "project_id": 5
    },

    # Project 6 - Viper Missile Guidance Software
    {
        "name": "Guidance Computer",
        "category": "Embedded System",
        "description": "Runs guidance algorithms using sensor inputs. Connected to inertial sensors and actuators via SPI and PWM interfaces.",
        "project_id": 6
    },
    {
        "name": "Actuator Control Module",
        "category": "Control Hardware",
        "description": "Controls fin actuators using signals from the guidance computer. Powered via dedicated DC supply and connected through control buses.",
        "project_id": 6
    },

    # Project 7 - Orion Sensor Fusion Engine
    {
        "name": "Fusion Processing Core",
        "category": "Software System",
        "description": "Aggregates sensor inputs from radar, IR, and EW systems over Ethernet. Performs real-time data fusion and outputs a unified situational picture.",
        "project_id": 7
    },
    {
        "name": "Sensor Interface Gateway",
        "category": "Interface System",
        "description": "Acts as middleware between physical sensors and processing core. Converts multiple protocols (CAN, UART, Ethernet) into a unified format.",
        "project_id": 7
    },

    # Project 8 - Titan Ground Radar Network
    {
        "name": "Radar Node Unit",
        "category": "Radar Hardware",
        "description": "Distributed radar node connected to central system via secure network. Includes antenna, receiver, and local processing unit.",
        "project_id": 8
    },
    {
        "name": "Network Coordination Server",
        "category": "Server System",
        "description": "Central server coordinating multiple radar nodes. Connected over secure IP network and responsible for data aggregation and control.",
        "project_id": 8
    },

    # Project 9 - Nova Secure Communications
    {
        "name": "Encryption Module",
        "category": "Security",
        "description": "Hardware-based encryption unit connected inline with communication interfaces. Secures all outgoing and incoming data streams.",
        "project_id": 9
    },
    {
        "name": "Radio Communication Unit",
        "category": "RF Communications",
        "description": "Handles wireless transmission using secure protocols. Connected to encryption module and external antenna system.",
        "project_id": 9
    },

    # Project 10 - EagleEye Target Tracking System
    {
        "name": "Tracking Algorithm Engine",
        "category": "Software",
        "description": "Runs AI-based tracking algorithms using incoming sensor data. Interfaces with sensor fusion system over Ethernet.",
        "project_id": 10
    },
    {
        "name": "Visualisation Console",
        "category": "User Interface",
        "description": "Displays tracked targets on operator screens. Connected to backend processing systems via network interface.",
        "project_id": 10
    }
]

insert_systems_q = """
    INSERT INTO Systems (name, category, description, project_id)
    VALUES (?, ?, ?, ?)
"""

systems_tuple = [
    (s["name"], s["category"], s["description"], s["project_id"])
    for s in systems
]

cursor.executemany(insert_systems_q, systems_tuple)
connection.commit()

select_systems_q = """
    SELECT name, category, description, project_id
    FROM Systems
"""

cursor.execute(select_systems_q)
rows = cursor.fetchall()
print(rows)

components = [
    {
        "name": "Raspberry Pi Compute Module 4",
        "type": "Processor",
        "part_number": "CM4-4GB-16GB",
        "unit_cost": 75.00
    },
    {
        "name": "STM32 Microcontroller",
        "type": "Microcontroller",
        "part_number": "STM32F407VGT6",
        "unit_cost": 12.50
    },
    {
        "name": "MPU-6050 IMU Sensor",
        "type": "Sensor",
        "part_number": "MPU6050",
        "unit_cost": 5.20
    },
    {
        "name": "Ublox GPS Module",
        "type": "Sensor",
        "part_number": "NEO-6M",
        "unit_cost": 18.00
    },
    {
        "name": "ADS-B Receiver Module",
        "type": "RF Module",
        "part_number": "ADS-B-RX1090",
        "unit_cost": 45.00
    },
    {
        "name": "2.4GHz RF Transceiver",
        "type": "Communication",
        "part_number": "NRF24L01+",
        "unit_cost": 3.50
    },
    {
        "name": "Ethernet PHY Module",
        "type": "Networking",
        "part_number": "LAN8720A",
        "unit_cost": 4.80
    },
    {
        "name": "CAN Bus Transceiver",
        "type": "Communication",
        "part_number": "MCP2551",
        "unit_cost": 2.10
    },
    {
        "name": "DC-DC Buck Converter",
        "type": "Power",
        "part_number": "LM2596S",
        "unit_cost": 2.75
    },
    {
        "name": "Lithium Polymer Battery",
        "type": "Power",
        "part_number": "LiPo-3S-5000mAh",
        "unit_cost": 35.00
    }
]

insert_components_q = """
    INSERT INTO Components (name, type, part_number, unit_cost)
    VALUES (?, ?, ?, ?)
"""

components_tuple = [
    (c["name"], c["type"], c["part_number"], c["unit_cost"])
    for c in components
]

cursor.executemany(insert_components_q, components_tuple)
connection.commit()

select_components_q = """
    SELECT name, type, part_number, unit_cost
    FROM Components
"""

cursor.execute(select_components_q)
rows = cursor.fetchall()

print(rows)

system_components = [
    {
        "component_id": 1,
        "system_id": 1
    },
    {
        "component_id": 2,
        "system_id": 1
    },
    {
        "component_id": 3,
        "system_id": 1
    },
    {
        "component_id": 4,
        "system_id": 1
    },
    {
        "component_id": 5,
        "system_id": 1
    },
    {
        "component_id": 6,
        "system_id": 1
    },
    {
        "component_id": 7,
        "system_id": 1
    },
    {
        "component_id": 8,
        "system_id": 1
    },
    {
        "component_id": 9,
        "system_id": 1
    },
    {
        "component_id": 10,
        "system_id": 1
    },
]

insert_system_components_q = """
    INSERT INTO SystemComponents (component_id, system_id)
    VALUES (?, ?)
"""

system_components_tuple = [
    (c["component_id"], c["system_id"])
    for c in system_components
]

cursor.executemany(insert_system_components_q, system_components_tuple)
connection.commit()

select_system_components_q = """
    SELECT component_id, system_id
    FROM SystemComponents
"""

cursor.execute(select_system_components_q)
rows = cursor.fetchall()

print(rows)

connections = [
    (1, 3, "I2C SDA", "SDA"),  # Pi CM4 ↔ MPU-6050
    (1, 3, "I2C SCL", "SCL"),  # Pi CM4 ↔ MPU-6050
    (1, 4, "UART TX", "RX"),   # Pi CM4 ↔ GPS
    (1, 4, "UART RX", "TX"),   # Pi CM4 ↔ GPS
    (1, 6, "SPI MOSI", "MOSI"),# Pi CM4 ↔ RF Transceiver
    (1, 6, "SPI MISO", "MISO"),# Pi CM4 ↔ RF Transceiver
    (1, 7, "Ethernet", "PHY"), # Pi CM4 ↔ Ethernet PHY Module
    (1, 9, "5V Power", "VIN"), # Pi CM4 ↔ DC-DC Buck Converter
    (1, 10, "Battery Input", "BATT"), # Pi CM4 ↔ LiPo Battery
    
    # STM32 connections
    (2, 3, "I2C SDA", "SDA"),  # STM32 ↔ MPU-6050
    (2, 3, "I2C SCL", "SCL"),  # STM32 ↔ MPU-6050
    (2, 4, "UART TX", "RX"),   # STM32 ↔ GPS
    (2, 4, "UART RX", "TX"),   # STM32 ↔ GPS
    (2, 6, "SPI MOSI", "MOSI"),# STM32 ↔ RF Transceiver
    (2, 6, "SPI MISO", "MISO"),# STM32 ↔ RF Transceiver
    (2, 8, "CAN_H", "CAN_H"),  # STM32 ↔ CAN Bus Transceiver
    (2, 8, "CAN_L", "CAN_L"),  # STM32 ↔ CAN Bus Transceiver
    
    # Power module connections
    (9, 10, "VOUT", "VIN"),    # DC-DC Buck ↔ LiPo Battery
    (9, 1, "VOUT 5V", "VIN"),  # DC-DC Buck ↔ Raspberry Pi CM4
    (10, 1, "Battery 3S", "VIN") # LiPo Battery ↔ Raspberry Pi CM4
]

# Insert query
insert_connections_q = """
    INSERT INTO Connections (system_component_a, system_component_b, component_a_label, component_b_label)
    VALUES (?, ?, ?, ?)
"""

cursor.executemany(insert_connections_q, connections)
connection.commit()

# Verify
cursor.execute("SELECT * FROM Connections")
rows = cursor.fetchall()
print(rows)