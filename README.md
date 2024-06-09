
# DIS Group Project
Repository for the group project in the course [Databases and Information Systems](https://kurser.ku.dk/course/ndab21010u) 
## Table of content
 - [Setup](#Setup)
	 - [Requirements](#Requirements)
	 - [Installation](#Installation) 
	 - [Initialization](#Initialization) 
	 - [Docker without Docker Desktop](#Docker-without-Docker-Desktop)
 - [Development](#Development)
	 - [Dependencies](#Dependencies)
	 - [Populating the database](#populating-the-database)
	 - [PGAdmin](#PGAdmin) 
	 - [Developing](#Developing)
	 - [Guidelines](#Guidelines)
 - [Running](#Running)
 - [E/R Diagram](#er-diagram)
 - [Usage](#Usage)

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
### Initialization
> [!NOTE]
> The project comes with PGAdmin and that is not a lightweight container. For teachers and TAs a more suitable  `compose.prod.yaml` compose file has been provided which omits PGAdmin.
#####  Windows:
```
git clone git@github.com:TimRJensen/dis-group-project.git
cd dis-group-project
mkdir src\secrets
python -c "import secrets;print(secrets.token_hex())" > src\secrets\flask-key
docker compose up -d
# without PGAdmin
docker compose -f compose.prod.yaml up -d
```
#####  Linux/ubunto:
```
git clone git@github.com:TimRJensen/dis-group-project.git
cd dis-group-project
mkdir src/secrets
python3 -c "import secrets;print(secrets.token_hex())" > src/secrets/flask-key
docker compose up -d
# without PGAdmin
docker compose -f compose.prod.yaml up -d
```
Confirm that the database is running with the following command:
```
docker exec postgres psql -U group77 -d uefa2024 -V
```
Confirm that the Flask server is running by navigating to [localhost:1234](http://localhost:1234?greet=name).
### Docker without Docker Desktop
Without Docker Desktop you'll need to install the Docker engine manually. You can follow one of [these](https://docs.docker.com/engine/install/) guides. Also remember to perform the [post installation](https://docs.docker.com/engine/install/linux-postinstall/) steps.
## Development
### Dependencies
Start by installing the application dependencies as a virtual environment:
#####  Windows:
```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```
#####  Linux/ubunto:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
### Populating the database
You should not need this step, but I include it for the sake of completeness.
##### Windows:
```
./bin/dm.exe populate
```
##### Linux/ubunto:
```
./bin/dm populate
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

Hit save and you're done. From tools you can try to select Query Tool and run some SQL queries against the database.
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
### With Docker
If you followed the initialization steps under installation, the web server should already be running at [localhost:1234](http://localhost:1234).

### Dockerless
> [!IMPORTANT]
> Running the application dockerless adds user "group77" and database "uefa2024" to your local PostgreSQL server.

Running the application dockerless assumes:
- A local PostgreSQL server.
- Root user is "postgres"
- Root password is "postgres"
- Server port is 5432

If you followed the initialization steps under installation up untill running Docker, you can run these commands to start the web server:
#####  Windows:
```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python run.py
```
#####  Linux/ubunto:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```
Then navigate to [localhost:5000](http://localhost:5000). 

## E/R Diagram
![er](https://github.com/TimRJensen/dis-group-project/assets/23018442/dbfb3fe9-8d92-4e71-bd44-89ee1cc2e789)

## Usage
The application is intended to be a statistical overview of the upcomming UEFA European Championship. As this is a future event, the data available to us are quite sparse. As of now it only reflect the group stages and fixtures, 
but as data becomes more readily available the database could easily be extended with the new data. As for interaction, it is for the most parts navigation between different segments of the application, by referencing the unique id
each entity has. We did however also add a search function, that will yield any fixtures that matches a teams name across localization. For example "ger dan" would yield fixtures for Denmark and Germany.

