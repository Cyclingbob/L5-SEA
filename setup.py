import subprocess

print("Creating DB tables...")
subprocess.run(["python", "setup_db.py"])
print("Inserting Sample data...")
subprocess.run(["python", "insert_example_data.py"])
print("Creating administrator user...")
subprocess.run(["python", "create_user.py", "Joe", "Bloggs", "joe@bloggs.com", "password123", "--admin"])
