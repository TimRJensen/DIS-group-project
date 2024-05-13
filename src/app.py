import psycopg, os 
from flask import Flask, render_template, request


app = Flask(__name__)
config = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

@app.get("/")
def index():
    with psycopg.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM version()")
            return render_template("index.html", 
                name=request.args.get("greet"), 
                psql_v=cursor.fetchone()[0])
 
if __name__ == "__main__":
    None