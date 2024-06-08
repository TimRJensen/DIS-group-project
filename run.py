"""
This script runs the Flask server in a dockerless environment.
As such, it makes these assumptions:
    - PostgreSQL is locally installed.
    - root user is "postgres" 
    - root password is "postgres" 
    - port is 5432 

Furthermore this will add the user "group77" & db "uefa2024" to your PostgreSQL server.
For convenience a sql script has been added to remove these entities:
psql -h localhost -U postgres -f schema/clean.sql
"""
from src import create_app, connect, con_config
from subprocess import run

if __name__ == "__main__":
    # Add user & db
    p = run(["psql", "-h", "localhost", "-U", "postgres", "-f", "schema/create.sql"], env={"PGPASSWORD": "postgres",})
    try:
        p.check_returncode()
    except:
        print("Failed to create user \"group77\" and database \"uefa2024\"\n"\
            "Please make sure your root user is \"postgres\", the password is \"postgres\" and that the server is running on port 5432" )
        exit(1)

    # If we're here everything's good and the below won't fail. Populate the db and connect.
    p = run(["psql", "-h", "localhost", "-U", con_config["user"], "-d", con_config["dbname"], "-f", "schema/init.sql"], env={"PGPASSWORD": con_config["password"]})
    con_config["host"] = "localhost"
    con_config["port"] = "5432"
    connect()

    # Start the app.
    create_app().run(debug=False)
    