# Product Design Tool (rename)
short description

# Usage instructions
It is necessary to complete setup instructions to ensure full function of the application.
## Setup

It is necessary to have Python 3 installed.
> The application has been implemented and tested using Python 3.13.3. It should function normally on older versions of Python 3, but this is not guarenteed.

1) Setup a virtual environment: `python -m venv venv`
> If `venv` is not found:<br>
> Windows: Reinstall Python<br>
> Debian/Ubuntu: `sudo apt-get install python3-venv`
2) Activate the virtual environment:<br>
Windows Command Prompt: `venv\Scripts\activate.bat`<br>
Windows Powershell: `venv\Scripts\Activate.ps1`<br>
Linux/Mac: `source venv/bin/activate`<r>

3) Install the required libraries: `pip install -r requirements.txt`
> `requirements.txt` describes the required packages to PIP.

4) Setup the database
Run `python setup_db.py`<br>
This will create all of the required tables for the SQLite database
> This uses the config file `config.py` for the name of the database file.

5) Add sample data
Run `python insert_example_data.py`<br>
This will insert sample data for the SQLite database
> This uses the config file `config.py` for the name of the database file.

6) Create an administrator user <br>
For security reasons, administrator users can only be created on the command line.<br>
Run `python create_user.py Joe Bloggs joe@bloggs.com secret_password --admin`
>The `--admin` flag tells SQLite that the user is an administator. Omitting this flag creates a regular user. This utility can only be run whilst the main application is not running.

7) Ensure that port `80` is not owned by any processes on your computer and free to be used by the main application. Close any applications using this port, or change the port in `config.py`

8) Setup is complete!


## Using the application
1) Run `python main.py` to start the FastAPI webserver.
2) Access [localhost](http://localhost)
3) You will be redirected to the login page.
4) Use the equivalent login details provided during setup, or any other users that have since been created.