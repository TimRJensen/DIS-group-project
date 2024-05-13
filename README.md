
# DIS Group Project
Repository for the group project in the course [Databases and Information Systems](https://kurser.ku.dk/course/ndab21010u) 
## Table of content
 - [Setup](#Setup)
	 - [Requirements](#Requirements)
	 - [Installation](#Installation) 
	 - [Docker without Docker Desktop](#DockerwithoutDockerDesktop)
 - [Development](#Development)
	 - [Initialization](#Initialization) 
	 - [Populating the database](#Populatingthedatabase)
	 - [PGAdmin](#PGAdmin) 
	 - [Developing](#Developing)
	 - [Guidelines](#Guidelines)
 - [Running](#Running)

## Setup
### Requirements
 - [Python](https://www.python.org/downloads/) v3.8 or newer (Flask requirement) & [pip](https://pip.pypa.io/en/stable/installation/)
 - [Docker Desktop](https://docs.docker.com/desktop/) v26.0.0

As an alternative to Docker Desktop, the engine can be installed seperately. This information is provided at the end of this section.
### Installation
Installation should be straightforward, with the exception that Docker Desktop requires you to sign up as a user. Once you have everything installed confirm that you can access everything from a terminal:
#####  Windows:
```
python --version
pip --version
docker --version
```
#####  Linux/ubunto:
```
python3 "--version"
pip --version
docker --version
```
### Docker without Docker Desktop
Without Docker Desktop you'll need to install the Docker engine manually. You can follow one of [these](https://docs.docker.com/engine/install/) guides. Also remember to perform the [post installation](https://docs.docker.com/engine/install/linux-postinstall/) steps.
## Development
### Initialization
#####  Windows:
```
git clone git@github.com:TimRJensen/dis-group-project.git
cd dis-group-project
docker compose up -d
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```
#####  Linux/ubunto:
```
git clone git@github.com:TimRJensen/dis-group-project.git
cd dis-group-project
docker compose up -d
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
Confirm that the database is running with the following command:
```
docker exec postgres psql -U group77 -d uefa2024 -V
```
Confirm that the Flask server is running by navigating to [localhost:1234](http://localhost:1234?greet=name). Lastly you need an evironment file, which you'll get from me. Place it under scripts/
### Populating the database
You should not need this step, but I include it for the sake of completeness.
##### Windows:
```
python scripts/datamanager.py populate
```
##### Linux/ubunto:
```
python3 scripts/datamanager.py populate
```
You only need to do this whenever the schema for the database changes. Besides populating the database, this script can also generate the current schema and restore the database from a backup. Run the script with the `--help` flag for more information.
### PGAdmin
You won't be able to access PGAdmin right away. It takes the container about a minute to initialize for the first time. You can follow the process in Docker Desktop by cliking on the container. Once it's ready navigate to [localhost:5050](http://localhost:5050). At the login page use the following:
- **Username**: group77@dis.com
- **Password**: dis2024

To connect to the database, rightclick Servers in the top left corner and select register server. In the general pane use whatever name you like. Switch to the connection pane and use the following:
- **Host name**: postgres
- **Port**: 5432
- **Maintenance database**: uefa2024
- **Password**: dis2024

Hit save and you're done. From tools you can try to select Query Tool and run some SQL commands against the database.
### Developing
Start the application services when you start developing:
#####  Windows/Linux/ubunto:
```
docker compose up -w
```
To stop the services press ctrl+c in the terminal where the services are running. Docker syncs the local repository with the remote flask container, which will reload the server, but not the page. To see your changes, hard refresh the page in the browser.
### Guidelines
 - Please dont force push to main.
 - When adding features, try to make them on a dev branch we all use or a new branch for that feature.

## Running
If you followed the setup section, you can start the application services with these commands:
#####  Windows/Linux/ubunto:
```
docker compose up -d
```
Then navigate to [localhost:1234](http://localhost:1234).
